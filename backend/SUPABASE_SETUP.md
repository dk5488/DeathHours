# Supabase Setup Guide

This backend uses PostgreSQL via Supabase as the primary database.

## Getting Your Supabase Connection String

1. Go to [Supabase Dashboard](https://app.supabase.com)
2. Select your project
3. Click **Settings** (gear icon, bottom left)
4. Click **Database** in the sidebar
5. Under **Connection String**, click the **URI** tab
6. Copy the connection string. It will look like:
   ```
   postgresql://postgres:[YOUR-PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres
   ```

## Setting up the Backend

1. Create a `.env` file in the `backend/` directory
2. Copy the Supabase connection string:
   ```bash
   DATABASE_URL=postgresql://postgres:[YOUR-PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres
   ```
3. Add other API keys as needed (Stripe, OpenWeatherMap, etc.)
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Run the backend:
   ```bash
   uvicorn main:app --reload
   ```

The database schema will be automatically created on first startup via `init_db()`.

## Database Administration

To view/manage your Supabase database:
- Use the **SQL Editor** in the Supabase dashboard
- Or connect with `psql` using the connection string
- Tables created:
  - `users`
  - `businesses`
  - `traffic_readings`
  - `events`
  - `alerts`
  - `action_cards`
  - `reports`
  - `competitors`
