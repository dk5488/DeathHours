"""Celery application instance & task autodiscovery for DeathHours.

All periodic/async jobs live under ``backend.workers.jobs``.  Importing this
module and calling :pyfunc:`celery_app.autodiscover_tasks` will make them
available to a worker process.  The broker URL can be controlled via the
``CELERY_BROKER_URL`` environment variable; Redis is used by default.
"""

import os
from celery import Celery

# allow the broker to be configured via env var, fall back to redis localhost
broker = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")

celery_app = Celery("deathhours", broker=broker)
# optional backend could be configured similarly with CELERY_RESULT_BACKEND

# automatically find tasks in jobs subpackage
celery_app.autodiscover_tasks([
    "backend.workers.jobs",
])

celery_app.conf.beat_schedule = {
    "fetch-busy-hours-daily": {
        "task": "busy_hours_job",
        "schedule": crontab(hour=0, minute=0),   # once per day
    },
}
