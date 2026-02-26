# Dead Hours Dashboard

A SaaS web application that helps small and medium-sized local businesses (restaurants, cafes, salons, retail shops) recover lost revenue by identifying predictable off-peak "dead hours" and providing actionable marketing recommendations.

## Mission
Bundle publicly available foot traffic data, weather signals, and local event feeds into a no-code dashboard with an automated suggestion engine, making business intelligence accessible and actionable for non-technical owners.

## High-level Architecture

The system will consist of three primary layers:

1. **Frontend** (Next.js + Tailwind CSS)
   - User interface with onboarding, dashboard, heatmaps, alerts, reports, settings.
   - Mobile-responsive, data-forward design.
   - Hosted on Vercel for fast delivery.

2. **Backend** (Python / FastAPI)
   - REST/GraphQL API powering data ingestion, processing, alerts, AI action generation, and reporting.
   - Integrations with third-party services (Outscraper, OpenWeatherMap, Eventbrite, Ticketmaster, Claude/GPT, Stripe, Supabase Auth).
   - Runs on Railway or similar PaaS.

3. **Data & Infrastructure**
   - PostgreSQL database (Supabase) for storing time-series foot traffic, user profiles, events, and analytics.
   - Background workers (Celery/RQ or serverless functions) to fetch/aggregate external data and generate AI recommendations.
   - Email/SMS via Resend/Twilio.

A small `docs/architecture.md` will capture component interactions and API boundaries.

## Next Steps
- Scaffold repositories for `frontend/` and `backend/` with initial readmes and minimal starter code.
- Define Supabase schema for business profiles, traffic records, events, alerts, and action cards.
- Set up CI/CD placeholders.

This repo will gradually grow as features are implemented over the planned 8‑week MVP timeline.

## Getting Started

1. **Frontend**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
2. **Backend**
   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   uvicorn main:app --reload
   ```

Environment variables should be defined in `backend/.env` (see `.env.example`).

Local development can proceed with the frontend hitting the backend at `http://localhost:8000` and the backend connecting to a local Postgres or Supabase instance.

