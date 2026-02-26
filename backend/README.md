# Backend

Python-based API using FastAPI. This service handles all business logic, data ingestion, AI suggestion generation, alerts, and integrations.

## Tech Stack
- Python 3.11+
- FastAPI
- Uvicorn/Gunicorn for ASGI server
- SQLAlchemy or `supabase-py` for database interactions
- Coverage/pytest for tests

## Setup

1. Create a virtual environment and install dependencies:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Set up your Supabase connection. See [SUPABASE_SETUP.md](./SUPABASE_SETUP.md) for detailed instructions.

3. Copy `.env.example` to `.env` and fill in your Supabase `DATABASE_URL`:

```bash
cp .env.example .env
# Edit .env with your DATABASE_URL
```

4. Run the server locally:

```bash
uvicorn main:app --reload
```

The database schema will be automatically initialized on startup.

## Structure

- `main.py` – FastAPI application entrypoint
- `models.py` – database models
- `schemas.py` – Pydantic schemas
- `routes/` – individual routers for different domains (businesses, traffic, events, alerts)
- `workers/` – background job definitions
- `utils/` – helper functions for external API calls
