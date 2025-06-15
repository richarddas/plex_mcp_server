#!/usr/bin/env python3
"""
Plex MCP Server - Main FastAPI application
"""

import asyncio
import json
import logging
import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from sse_starlette import EventSourceResponse
import uvicorn

from config import config, Config
from plex_client import plex_client
from mcp_handler import mcp_handler

# Setup logging
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Store for SSE connections and message queues
connections = {}
message_queues = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    Config.validate()
    logger.info(f"Connected to Plex server: {plex_client.server_name}")
    logger.info(f"Starting Plex MCP Server on {config.HOST}:{config.PORT}")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Plex MCP Server")

# FastAPI app
app = FastAPI(
    title="Plex MCP Server",
    description="Model Context Protocol server for Plex media management",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Plex MCP Server",
        "server": plex_client.server_name,
        "version": "1.0.0"
    }

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy", "server": plex_client.server_name}

@app.get("/sse")
async def sse_endpoint(request: Request):
    """SSE endpoint for MCP connections"""
    client_id = str(uuid.uuid4())
    message_queues[client_id] = asyncio.Queue()
    
    logger.info(f"New SSE connection: {client_id}")
    
    async def event_stream():
        try:
            # Send initial connection established message
            yield {
                "data": json.dumps({
                    "jsonrpc": "2.0",
                    "method": "notifications/initialized",
                    "params": {}
                })
            }
            
            # Listen for messages in the queue
            while True:
                try:
                    # Wait for messages with timeout
                    message = await asyncio.wait_for(
                        message_queues[client_id].get(),
                        timeout=30.0
                    )
                    yield {"data": json.dumps(message)}
                except asyncio.TimeoutError:
                    # Send keepalive
                    yield {"data": "keepalive"}
                    
        except asyncio.CancelledError:
            logger.info(f"SSE connection closed: {client_id}")
        finally:
            # Cleanup
            if client_id in message_queues:
                del message_queues[client_id]
            if client_id in connections:
                del connections[client_id]
    
    connections[client_id] = request
    return EventSourceResponse(event_stream())

@app.post("/sse")
async def sse_post_endpoint(request: Request):
    """Handle POST requests to SSE endpoint (for mcp-remote compatibility)"""
    try:
        message = await request.json()
        logger.debug(f"Received POST to /sse: {message}")
        
        # Handle the message using MCP handler
        response = mcp_handler.handle_message(message)
        
        # If there are active connections, send the response via SSE
        for client_id in list(message_queues.keys()):
            try:
                await message_queues[client_id].put(response)
            except Exception as e:
                logger.error(f"Error sending to client {client_id}: {e}")
        
        # Also return the response directly
        return response
        
    except Exception as e:
        logger.error(f"Error in SSE POST handler: {e}")
        return {
            "jsonrpc": "2.0",
            "id": None,
            "error": {"code": -32700, "message": "Parse error"}
        }

@app.post("/messages")
async def handle_messages(request: Request):
    """Handle MCP messages (alternative endpoint)"""
    try:
        message = await request.json()
        logger.debug(f"Received message: {message}")
        
        response = mcp_handler.handle_message(message)
        logger.debug(f"Sending response: {response}")
        
        return response
        
    except Exception as e:
        logger.error(f"Error in message handler: {e}")
        return {
            "jsonrpc": "2.0",
            "id": None,
            "error": {"code": -32700, "message": "Parse error"}
        }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=config.HOST,
        port=config.PORT,
        reload=False,
        log_level=config.LOG_LEVEL.lower()
    )
