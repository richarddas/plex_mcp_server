# Plex MCP Server

A Model Context Protocol (MCP) server for Plex media management, enabling AI assistants like Claude to interact with your Plex library.

## Features

- **Movie Management**: Search, browse, and analyze your movie collection
- **Library Statistics**: Get insights into your media collection
- **Genre & Director Search**: Find content by specific criteria
- **Recent Additions**: Track newly added content
- **Extensible Architecture**: Easy to add TV shows and other media types

## Requirements

- Python 3.8 or higher
- Plex Media Server with accessible API
- Network access to your Plex server

## Setup

### Quick Setup (Recommended)

```bash
# Clone the repository
git clone https://github.com/richarddas/plex_mcp_server.git
cd plex_mcp_server

# Run the setup script (creates venv and installs dependencies)
./setup.sh

# Edit your Plex details
nano .env

# Activate virtual environment and start the server
source venv/bin/activate
python main.py
```

### Manual Setup

1. **Create and activate virtual environment**:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install dependencies**:

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. **Configure environment variables**:

   ```bash
   cp .env.example .env
   nano .env
   ```

   Update the values in `.env`:

   - `PLEX_URL`: Your Plex server URL (e.g., `http://192.168.1.100:32400`)
   - `PLEX_TOKEN`: Your Plex authentication token ([How to find it](https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/))
   - `HOST` and `PORT`: Server binding (defaults are fine for most setups)
   - `LOG_LEVEL`: Logging verbosity (INFO recommended)

4. **Run the server**:
   ```bash
   python main.py
   ```

### Daily Usage

After initial setup, to run the server:

```bash
cd plex-mcp-server
source venv/bin/activate  # Activate virtual environment
python main.py            # Start server
# When done: deactivate   # Exit virtual environment
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
