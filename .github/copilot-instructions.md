# Riot App Backend - AI Coding Assistant Instructions

## Architecture Overview

This is a FastAPI-based backend for querying Riot Games League of Legends API. The application follows a layered architecture:

- **`app/main.py`** - Entry point; initializes FastAPI application and registers routes
- **`app/core/config.py`** - Configuration management using Pydantic; loads `RIOT_API_KEY` from `.env`
- **`app/routes/`** - API route handlers; organize endpoints by resource (e.g., `/routes/player.py` for player-related endpoints)
- **`app/services/`** - Business logic layer:
  - `cache.py` - Caching abstraction for reducing Riot API calls
  - `riot_client.py` - Wrapper for Riot API interactions; handles authentication and HTTP requests

## Data Flow & Integration Pattern

1. **Request Entry**: FastAPI routes in `app/routes/` receive incoming HTTP requests
2. **Service Layer**: Routes call service functions from `app/services/` (e.g., `riot_client.get_summoner()`)
3. **Riot API Integration**: `riot_client.py` constructs authenticated requests using `RIOT_API_KEY` from config
4. **Caching Strategy**: `cache.py` intercepts service calls to avoid redundant API requests; cache keys typically combine endpoint + parameters
5. **Response Flow**: Services return parsed data; routes serialize to JSON

**Example Pattern**: `GET /player/{name}` → `player.py` route → `riot_client.get_summoner_by_name(name)` → check `cache.get()` → call Riot API if cache miss → `cache.set()` → return response

## Development Conventions

### Environment & Dependencies
- Python 3.9+; use `pip` for package management
- `.env` file required with `RIOT_API_KEY` from [Riot Developer Portal](https://developer.riotgames.com/)
- Install dependencies: `pip install fastapi uvicorn requests pydantic python-dotenv`

### API Route Pattern
- Define routes in `app/routes/{resource}.py` files (one file per logical resource)
- Use path parameters sparingly; prefer query parameters for filtering
- Example: `app/routes/player.py` exports a FastAPI `APIRouter`
- Inject services via dependency injection in route handlers

### Service Layer Pattern
- Create service classes/functions in `app/services/` for reusable business logic
- `riot_client.py` should be the **only** place making HTTP calls to external APIs
- All Riot API keys and secrets stay in `config.py`; never hardcode credentials
- Service functions should handle errors gracefully (rate limits, timeouts) and raise custom exceptions

### Caching Pattern
- Implement cache as a key-value abstraction (supports Redis or in-memory backends)
- Cache keys: `f"{resource_type}:{identifier}"` (e.g., `"summoner:NA1:Faker"`)
- TTL (time-to-live) per resource type: summoner data ~24h, match data ~7d, static data ~1 month
- Clear cache on configuration changes or after mutations

## Critical Developer Workflows

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run server with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Test a route
curl "http://localhost:8000/player/Faker"
```

### Testing Strategy
- Unit tests: test service logic in isolation with mock Riot API responses
- Integration tests: test full request path without calling live Riot API
- Use fixtures for common test data (summoner objects, match histories)

### Debugging Tips
- Enable uvicorn logging: check startup errors and request logs
- Riot API rate limits: 120 requests/minute; implement exponential backoff in `riot_client.py`
- Cache misses cause slowdowns; validate cache key consistency

## Project-Specific Patterns

### Naming Conventions
- Resource names (routes, service functions) match Riot API terminology: "summoner", "match", "champion" (not "player")
- Python module names: lowercase with underscores (e.g., `riot_client.py`, not `riotClient.py`)
- API endpoint paths: plural nouns (e.g., `/summoners/{name}`, not `/summoner/{name}`)

### Error Handling
- Raise descriptive exceptions in services; let routes handle HTTP status mapping
- Example: `RiotAPIError` for external API failures (404, 429, 500), `CacheError` for cache layer issues
- Always return 5xx responses for unrecoverable errors; 4xx for client input validation

### Configuration
- Use Pydantic `BaseSettings` in `config.py` to validate and document required environment variables
- Never access `os.environ` directly outside `config.py`; inject config object into services

## Key Integration Points

- **Riot API**: Async HTTP calls via `requests` or `httpx` library in `riot_client.py`
- **Cache Backend**: Pluggable (Redis by default for production; in-memory for dev)
- **Logging**: Use Python's `logging` module; configure in `main.py` startup
