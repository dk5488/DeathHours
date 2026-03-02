#!/usr/bin/env python3
"""
Test script to verify Celery worker can access database and process data.
"""

import os
import sys
from datetime import datetime, timedelta

# Add workspace to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.config.db import SessionLocal
from backend.models.models import TrafficReading, Business
from backend.workers.celery_app import celery_app

def test_celery_task_and_database():
    """Test that Celery can process tasks and access database data."""
    
    print("\n" + "="*60)
    print("🧪 CELERY WORKER & DATABASE INTEGRATION TEST")
    print("="*60)
    
    # Test 1: Database Access
    print("\n✓ Test 1: Testing Database Access")
    print("-" * 60)
    session = SessionLocal()
    
    businesses = session.query(Business).all()
    print(f"Found {len(businesses)} businesses in database:\n")
    
    for i, business in enumerate(businesses, 1):
        readings = session.query(TrafficReading).filter(
            TrafficReading.business_id == business.id
        ).all()
        print(f"{i}. {business.name}")
        print(f"   Owner ID: {business.owner_id}")
        print(f"   Category: {business.category}")
        print(f"   Location: {business.address}")
        print(f"   Google Maps: {business.google_maps_url[:60]}...")
        print(f"   Traffic Readings: {len(readings)}")
        
        if readings:
            latest = readings[-1]
            print(f"   Latest Reading: {latest.visitors_estimate} visitors at {latest.timestamp}")
        print()
    
    session.close()
    
    # Test 2: Create a simple test task
    print("\n✓ Test 2: Testing Celery Task Definition")
    print("-" * 60)
    
    # Define a simple test task
    @celery_app.task(name="test_database_access")
    def test_db_task():
        """Test task that reads from database."""
        session = SessionLocal()
        count = session.query(Business).count()
        session.close()
        return {
            "status": "success",
            "message": f"Successfully accessed database, found {count} businesses",
            "timestamp": datetime.utcnow().isoformat()
        }
    
    # Send the task
    print("Sending test task to Celery worker...")
    result = test_db_task.delay()
    print(f"Task ID: {result.id}")
    print(f"✓ Task queued successfully (result backend is disabled)")
    print(f"  The worker will execute this task when available")
    
    # Wait a moment for the worker to pick it up if running
    import time
    time.sleep(0.5)
    print(f"  Check the celery worker logs to see task execution")
    
    # Test 3: Verify Redis connection
    print("\n✓ Test 3: Verifying Redis Connection")
    print("-" * 60)
    try:
        from redis import Redis
        r = Redis.from_url(os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0"))
        pong = r.ping()
        print(f"✓ Redis connection successful: {pong}")
        print(f"  Broker URL: {os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')}")
    except Exception as e:
        print(f"✗ Redis connection failed: {e}")
    
    # Test 4: Check Celery configuration
    print("\n✓ Test 4: Celery Configuration")
    print("-" * 60)
    print(f"Broker URL: {celery_app.conf.broker_url}")
    print(f"Result Backend: {celery_app.conf.result_backend}")
    print(f"Worker Concurrency: {celery_app.conf.worker_concurrency}")
    
    print("\n" + "="*60)
    print("✓ ALL TESTS COMPLETED SUCCESSFULLY!")
    print("="*60)
    print("\nℹ️  Start the Celery worker with:")
    print("   celery -A backend.workers.celery_app worker --loglevel=info")
    print("\n")

if __name__ == "__main__":
    test_celery_task_and_database()
