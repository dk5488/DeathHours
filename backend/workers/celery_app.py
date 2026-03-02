"""Celery application instance & task autodiscovery for DeathHours.

All periodic/async jobs live under ``backend.workers.jobs``.  Importing this
module and calling :pyfunc:`celery_app.autodiscover_tasks` will make them
available to a worker process.  The broker URL can be controlled via the
``CELERY_BROKER_URL`` environment variable; Redis is used by default.
"""

import os
from celery import Celery
from celery.schedules import crontab
import importlib
import pkgutil

# allow the broker to be configured via env var, fall back to redis localhost
broker = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")

celery_app = Celery("deathhours", broker=broker)
# optional backend could be configured similarly with CELERY_RESULT_BACKEND

# Ensure all job modules are imported so tasks are registered with the worker.
# Celery's autodiscover looks for "tasks" modules by default; our jobs
# live in multiple modules under backend.workers.jobs, so import them.
try:
    jobs_pkg = importlib.import_module("backend.workers.jobs")
    for finder, name, ispkg in pkgutil.iter_modules(jobs_pkg.__path__):
        importlib.import_module(f"backend.workers.jobs.{name}")
except Exception:
    # best-effort import; if it fails tasks should still be discovered
    pass

celery_app.conf.beat_schedule = {
    "fetch-busy-hours-daily": {
        "task": "busy_hours_job",
        "schedule": crontab(hour=0, minute=0),   # once per day
    },
}
