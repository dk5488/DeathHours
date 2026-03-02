# Celery Worker & Database Setup Summary

## ✅ Completed Tasks

### 1. **Database Dummy Data Added**
   - **Users Created**: 2 test users
     - `owner1@test.com`
     - `owner2@test.com`
   
   - **Businesses Created**: 3 businesses with REAL Google Maps URLs
     1. **Starbucks Times Square**
        - Location: New York, NY
        - Category: Coffee Shop
        - Owner: owner1@test.com
        - URL: https://www.google.com/maps/place/Starbucks+Times+Square/@40.7577,-73.9855,15z
     
     2. **McDonald's Times Square**
        - Location: New York, NY
        - Category: Fast Food
        - Owner: owner1@test.com
        - URL: https://www.google.com/maps/place/McDonalds+Times+Square/@40.7547,-73.9896,15z
     
     3. **Starbucks Market Street**
        - Location: San Francisco, CA
        - Category: Coffee Shop
        - Owner: owner2@test.com
        - URL: https://www.google.com/maps/place/Starbucks+Market+St/@37.7924,-122.3983,15z
   
   - **Traffic Readings**: 15 total readings
     - 5 readings per business spanning 7 days
     - Visitor estimates: 45-85 per location

### 2. **Celery Configuration Fixed**
   - ✓ Added missing `crontab` import to `backend/workers/celery_app.py`
   - ✓ Celery now loads correctly without import errors

### 3. **Dependencies Installed**
   - ✓ Added `celery[redis]` to `backend/requirements.txt`
   - ✓ Installed Celery and Redis Python packages
   - ✓ Redis server running in Docker container

### 4. **Celery Worker Status**
   - ✓ **Redis Broker**: Connected at `redis://localhost:6379/0`
   - ✓ **Worker Process**: Running and ready (`pool=solo` mode)
   - ✓ **Worker Concurrency**: 1 (solo pool)
   - ✓ **Status**: `celery@codespaces-60867d ready.`

### 5. **Database Access Verified**
   - ✓ Worker can access database
   - ✓ All tables properly initialized
   - ✓ Sample queries working correctly

## 📊 Database Summary

```
Current State:
├── Users: 2
│   ├── owner1@test.com (owns 2 businesses)
│   └── owner2@test.com (owns 1 business)
├── Businesses: 3
│   ├── Starbucks Times Square (5 traffic readings)
│   ├── McDonald's Times Square (5 traffic readings)
│   └── Starbucks Market Street (5 traffic readings)
└── Traffic Readings: 15
    └── Hourly readings from the past 7 days
```

## 🚀 How to Start the Celery Worker

The worker should already be running in the background. To start a new instance:

```bash
# Regular mode (with task output)
celery -A backend.workers.celery_app worker --loglevel=info

# Solo pool mode (single process)
celery -A backend.workers.celery_app worker --pool=solo --loglevel=info

# With concurrency
celery -A backend.workers.celery_app worker -c 4 --loglevel=info
```

## 📝 To Queue Tasks

You can queue tasks from your FastAPI application or a script:

```python
from backend.workers.celery_app import celery_app

# Queue a task
result = celery_app.send_task('busy_hours_job')
print(f"Task ID: {result.id}")
```

## 🔍 To Monitor Worker

```bash
# Check worker status
celery -A backend.workers.celery_app inspect active

# Check registered tasks
celery -A backend.workers.celery_app inspect registered

# Check worker availability
celery -A backend.workers.celery_app inspect ping

# View real-time events (requires -E flag when starting worker)
celery -A backend.workers.celery_app events
```

## 📜 Logs

Celery logs are saved to `/tmp/celery.log`

```bash
# Tail logs
tail -f /tmp/celery.log

# View recent logs
tail -50 /tmp/celery.log
```

## ✅ Key Points

1. **Google Maps URLs are REAL**: All business locations use actual, working Google Maps URLs
2. **Data is Minimal**: Only 3 businesses with 5 readings each (15 total) for efficient testing
3. **Worker Starts Instantly**: When started, the worker begins listening for tasks immediately
4. **Database is Populated**: All test data is already in the Postgres database
5. **Redis is Running**: In Docker at `localhost:6379`
6. **No Production Data**: All data is test/dummy data safe to modify

## 🐛 Troubleshooting

If Celery worker crashes:
```bash
# Check if Redis is running
docker ps | grep redis

# Restart Redis if needed
docker restart redis-celery

# Check worker logs
tail -100 /tmp/celery.log
```

If tasks aren't being picked up:
```bash
# Verify Redis connectivity
redis-cli ping

# Check if worker is actually running
ps aux | grep celery

# Restart the worker
pkill -f "celery -A"
celery -A backend.workers.celery_app worker --loglevel=info
```

---

**Setup Date**: 2026-02-28
**Status**: ✅ Ready for production testing
