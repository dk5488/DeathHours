# Architecture Overview

This document outlines the core components and data flows for Dead Hours Dashboard.

## Components

- **Frontend (Next.js)**
  - Public pages for marketing and login/signup.
  - Private dashboard screens: heatmap, competitors, events, reports, settings.
  - Authentication via Supabase Auth or Clerk.
  - Communicates with backend API for data retrieval and subscriptions.

- **Backend (FastAPI)**
  - Provides REST endpoints for: business setup, traffic queries, event lookups, AI suggestions, reports, and alert configuration.
  - Scheduled tasks fetch external data (foot traffic, weather, events) and store normalized records.
  - Worker functions generate weekly reports and trigger email/SMS alerts.
  - Integrates with Stripe for billing and subscription management.

- **Database (PostgreSQL via Supabase)**
  - Tables: `users`, `businesses`, `traffic_readings`, `events`, `alerts`, `action_cards`, `reports`.
  - Time-series indexes on `traffic_readings` for efficient heatmap queries.

- **External APIs**
  - Foot traffic: Outscraper or PopulationMap pulled periodically.
  - Weather: OpenWeatherMap for current/forecast data.
  - Events: Eventbrite and Ticketmaster feeds.
  - AI: Claude or GPT for generating marketing copy.
  - Messaging: Resend for email, Twilio for SMS.

- **Infrastructure**
  - Frontend deployed to Vercel.
  - Backend hosted on Railway or similar.
  - Background jobs via Celery or serverless cron functions.
  - Monitoring and logging via built-in PaaS tools.

## Data Flow

1. Business owner registers and provides Google Maps URL.
2. Backend normalizes business info and schedules data collection.
3. Periodic tasks scrape popular-times data, store readings.
4. Weather and events data are correlated and added to the database.
5. Prediction algorithms identify upcoming dead hours.
6. AI engine consumes signals and generates action cards.
7. Alerts dispatched based on user preferences.
8. Frontend consumes API to render dashboards, heatmaps, and reports.

## Deployment & CI

- Separate pipelines for frontend and backend.
- Use GitHub Actions to run linting, tests, and build artifacts.
- Deploy triggered on merges to `main`.

This document will be expanded with diagrams and detailed endpoint specifications as the project evolves.