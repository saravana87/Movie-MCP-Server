# Movie MCP Server

A Model Context Protocol (MCP) server that provides access to a comprehensive movie database and web search capabilities. This server allows AI assistants to search for movie information from a local CSV database and perform web searches for current movie information.

## 🚀 Features

- **Local Movie Database**: Search through 4800+ movies with detailed information including cast, crew, budget, ratings, and more
- **Enhanced Search**: Fuzzy matching and intelligent search that handles partial titles and typos
- **Web Search Integration**: Search for current movie information using Serper API
- **Multiple Output Formats**: Supports both SSE (Server-Sent Events) and STDIO transport
- **Robust Error Handling**: Comprehensive logging and error management
- **Environment Configuration**: Flexible configuration via environment variables

## 📦 Requirements

- Python 3.8+
- pandas
- httpx  
- beautifulsoup4
- python-dotenv
- mcp (Model Context Protocol library)

## 🛠️ Installation

1. **Clone the repository:**
```bash
git clone https://github.com/saravana87/Movie-MCP-Server.git
cd Movie-MCP-Server
```

2. **Create and activate a virtual environment:**
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements-clean.txt
```

4. **Set up environment variables:**
Create a `.env` file in the project root:
```env
# Required for web search functionality
SERPER_API_KEY=your_serper_api_key_here

# Optional configurations
MOVIES_CSV_PATH=movies.csv
MAX_SEARCH_RESULTS=5
REQUEST_TIMEOUT=30
```

**Getting a Serper API Key:**
1. Visit [serper.dev](https://serper.dev)
2. Sign up for a free account
3. Get your API key from the dashboard
4. Add it to your `.env` file

## 🚀 Running the Server

### Basic Usage
```bash
python mcp_moviedb_server.py
```

### With Custom Configuration
```bash
# Run with SSE transport on custom port
python mcp_moviedb_server.py --server_type sse --port 8080 --host 0.0.0.0

# Run with STDIO transport
python mcp_moviedb_server.py --server_type stdio
```

## 🔧 Available Tools

### 1. `get_movie_info`
Search for movies in the local database.

**Parameters:**
- `title` (string): Movie title to search for
- `limit` (int, optional): Maximum number of results (default: 5)

**Example:**
```python
get_movie_info("Avatar", limit=3)
```

### 2. `search_web`
Search the web for current movie information.

**Parameters:**
- `query` (string): Search query
- `num_results` (int, optional): Number of results (default: 2, max: 10)

**Example:**
```python
search_web("latest Marvel movies 2024", num_results=5)
```

### 3. `get_movie_stats`
Get statistics about the movie database.

**Example:**
```python
get_movie_stats()
```

## 📊 Movie Database

The server includes a comprehensive movie dataset with:
- **4800+ movies** from various years and genres
- **Detailed information**: Title, release date, overview, genres, cast, crew, director, budget, revenue, ratings, and more
- **Rich metadata**: Production companies, countries, languages, keywords

## 🔧 Configuration Options

Environment variables for customization:

| Variable | Default | Description |
|----------|---------|-------------|
| `SERPER_API_KEY` | None | API key for web search (required for web search) |
| `MOVIES_CSV_PATH` | `movies.csv` | Path to the movie database CSV file |
| `MAX_SEARCH_RESULTS` | `5` | Maximum results for movie searches |
| `REQUEST_TIMEOUT` | `30` | Timeout for web requests (seconds) |

## 🐛 Troubleshooting

### Common Issues

1. **Import Error: No module named 'mcp'**
   ```bash
   pip install mcp
   ```

2. **Movie database not found**
   - Ensure `movies.csv` is in the project directory
   - Check the `MOVIES_CSV_PATH` environment variable

3. **Web search not working**
   - Verify your `SERPER_API_KEY` is set correctly
   - Check your internet connection
   - Ensure you have remaining API credits

4. **Server won't start**
   - Check that the port isn't already in use
   - Verify all dependencies are installed
   - Check the logs for specific error messages

## 📝 Logs

The server provides detailed logging for debugging:
- INFO level: General operations and search queries
- ERROR level: Failed operations and exceptions
- WARN level: Configuration issues

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## 🔗 Related Links

- [Model Context Protocol (MCP)](https://github.com/modelcontextprotocol)
- [Serper API Documentation](https://serper.dev/api-documentation)
- [FastMCP Framework](https://github.com/jlowin/fastmcp)

