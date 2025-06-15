# Plex MCP Server

A Model Context Protocol (MCP) server for Plex media management, enabling AI assistants like Claude to interact with your Plex library.

## Features

- **Movie Management**: Search, browse, and analyze your movie collection
- **Library Statistics**: Get insights into your media collection
- **Genre & Director Search**: Find content by specific criteria
- **Recent Additions**: Track newly added content
- **Extensible Architecture**: Easy to add TV shows and other media types

## Setup

1. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment variables**:
   Create a `.env` file:

   ```
   PLEX_URL=http://your-plex-server:32400
   PLEX_TOKEN=your-plex-token
   HOST=0.0.0.0
   PORT=8000
   LOG_LEVEL=INFO
   ```

3. **Run the server**:
   ```bash
   python main.py
   ```

## Claude Desktop Configuration

Add to your Claude Desktop `config.json`:

```json
{
  "globalShortcut": "",
  "mcpServers": {
    "plex": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "http://your-server:8000/sse",
        "--allow-http"
      ]
    }
  }
}
```

## Available Tools

### Movie Tools

- `get_library_stats` - Overall library statistics
- `list_all_movies` - Browse all movies with pagination
- `search_movies` - Search by title
- `search_by_genre` - Find movies by genre
- `search_by_director` - Find movies by director
- `search_by_year_range` - Find movies by year range
- `get_all_genres` - List all available genres
- `get_all_directors` - List all directors
- `get_recent_movies` - Recently added movies

## Project Structure

```
plex_mcp_server/
├── main.py              # FastAPI server
├── config.py            # Configuration
├── plex_client.py       # Plex connection
├── mcp_handler.py       # MCP message handling
├── tools/
│   ├── movie_tools.py   # Movie-related tools
│   └── tv_tools.py      # TV tools (future)
└── requirements.txt     # Dependencies
```

## Development

To add new tools:

1. Add methods to the appropriate tools file
2. Update the `get_tool_definitions()` method
3. Register the tool in `mcp_handler.py`

## License

MIT License
