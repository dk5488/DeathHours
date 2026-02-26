# Backend

Python-based API using FastAPI. This service handles all business logic, data ingestion, AI suggestion generation, alerts, and integrations.

## Tech Stack
- Python 3.11+
- FastAPI
- Uvicorn/Gunicorn for ASGI server
- SQLAlchemy or `supabase-py` for database interactions
- Coverage/pytest for tests

## Setup

Create a virtual environment and install dependencies:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install fastapi uvicorn
```

Add other packages such as `httpx`, `celery`, `stripe`, etc. as needed.

Run the server locally:

```bash
uvicorn main:app --reload
```

## Structure

- `main.py` – FastAPI application entrypoint
- `models.py` – database models
- `schemas.py` – Pydantic schemas
- `routes/` – individual routers for different domains (businesses, traffic, events, alerts)
- `workers/` – background job definitions
- `utils/` – helper functions for external API calls
