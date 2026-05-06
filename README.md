# Claude SDK Agent

A FastAPI-based agent that uses the Anthropic Claude SDK to perform automated tasks with tool integration.

## Project Structure

```
anthropic-claude-sdk-agent/
├── agent/
│   └── agent.py           # Standalone CLI agent script
├── api/
│   ├── __init__.py        # API package init
│   └── app.py             # FastAPI application with HTTP endpoints
├── Dockerfile             # Docker image definition
├── docker-compose.yml     # Docker Compose configuration
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (API key)
└── README.md              # This file
```

## Setup

### Prerequisites

- Docker and Docker Compose installed
- Anthropic API key

### Environment Configuration

Create a `.env` file in the project root:

```
ANTHROPIC_API_KEY=sk-ant-your-actual-api-key-here
```

Replace `sk-ant-your-actual-api-key-here` with your actual Anthropic API key from [console.anthropic.com](https://console.anthropic.com).

## Running with Docker

### Start the API server

```bash
docker compose up --build
```

The FastAPI server will start on `http://localhost:8000`.

### Stop the server

```bash
docker compose down
```

## API Endpoints

### Health Check

Check if the server is running:

```bash
curl http://localhost:8000/
```

**Response:**
```json
{
  "status": "ok"
}
```

### Query Endpoint

Send a prompt to Claude agent:

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Review utils.py for bugs that would cause crashes. Fix any issues you find.",
    "allowed_tools": ["Read", "Edit", "Glob"],
    "permission_mode": "acceptEdits"
  }'
```

**Request Body:**
- `prompt` (string, required): The task description for Claude
- `allowed_tools` (array, optional): Tools Claude can use. Options: `["Read", "Edit", "Glob"]`
- `permission_mode` (string, optional): How to handle tool execution. Default: `"acceptEdits"`

**Response:**
```json
{
  "response": "Claude's response and tool execution results...",
  "done": true,
  "error": null
}
```

### Custom Prompt Example

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "List all Python files in the project",
    "allowed_tools": ["Glob"],
    "permission_mode": "acceptEdits"
  }'
```

## Running Standalone Agent

To run the CLI agent directly (without API):

```bash
docker run --env-file .env claude-sdk-agent python agent/agent.py
```

Or build and run:

```bash
docker build -t claude-sdk-agent .
docker run --env-file .env claude-sdk-agent python agent/agent.py
```

## API Documentation

Once the server is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Troubleshooting

### API Key Error

If you see `Command failed with exit code 1`, ensure:
1. Your `.env` file has a valid `ANTHROPIC_API_KEY`
2. The key starts with `sk-ant-`

Check container logs:
```bash
docker compose logs -f
```

### Port Already in Use

If port 8000 is already in use, update `docker-compose.yml`:

```yaml
ports:
  - "8001:8000"  # Changed host port to 8001
```

Then access the API on `http://localhost:8001`.

## Dependencies

- `claude-agent-sdk` - Anthropic Claude SDK
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `python-dotenv` - Environment variable management
- `pydantic` - Data validation

## License

MIT
