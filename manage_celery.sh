#!/bin/bash
# Helper script to manage Celery worker and database setup

set -e

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 DeathHours Celery Manager${NC}\n"

case "${1:-help}" in
  start)
    echo "Starting Redis and Celery worker..."
    
    # Check if Redis container exists
    if ! docker inspect redis-celery >/dev/null 2>&1; then
      echo "Creating Redis container..."
      docker run -d --name redis-celery -p 6379:6379 redis:latest
    else
      # If exists but not running, start it
      if ! docker ps | grep -q redis-celery; then
        docker start redis-celery
      fi
    fi
    
    echo -e "${GREEN}✓${NC} Redis running on localhost:6379"
    
    # Kill existing workers
    pkill -f "celery -A" 2>/dev/null || true
    sleep 1
    
    # Start worker
    cd "$(dirname "$0")" || exit 1
    celery -A backend.workers.celery_app worker --loglevel=info --pool=solo > /tmp/celery.log 2>&1 &
    sleep 2
    
    if pgrep -f "celery -A" > /dev/null; then
      echo -e "${GREEN}✓${NC} Celery worker started (PID: $(pgrep -f "celery -A" | head -1))"
      echo ""
      echo "Log file: /tmp/celery.log"
      echo "View logs: tail -f /tmp/celery.log"
    else
      echo -e "${RED}✗${NC} Failed to start worker"
      cat /tmp/celery.log
      exit 1
    fi
    ;;

  stop)
    echo "Stopping Celery worker and Redis..."
    pkill -f "celery -A" 2>/dev/null || true
    docker stop redis-celery 2>/dev/null || true
    echo -e "${GREEN}✓${NC} Services stopped"
    ;;

  restart)
    "$0" stop
    sleep 1
    "$0" start
    ;;

  status)
    echo "System Status:"
    echo "-----------"
    
    # Redis status
    if docker ps | grep -q redis-celery; then
      echo -e "${GREEN}✓${NC} Redis: Running"
    else
      echo -e "${RED}✗${NC} Redis: Not running"
    fi
    
    # Worker status
    if pgrep -f "celery -A" > /dev/null; then
      PID=$(pgrep -f "celery -A" | head -1)
      echo -e "${GREEN}✓${NC} Celery Worker: Running (PID: $PID)"
    else
      echo -e "${RED}✗${NC} Celery Worker: Not running"
    fi
    
    # Database status
    cd "$(dirname "$0")" || exit 1
    if python -c "from backend.config.db import SessionLocal; SessionLocal().close()" 2>/dev/null; then
      echo -e "${GREEN}✓${NC} Database: Connected"
    else
      echo -e "${RED}✗${NC} Database: Connection failed"
    fi
    ;;

  logs)
    if [ -f /tmp/celery.log ]; then
      tail -f /tmp/celery.log
    else
      echo "No logs found. Start the worker first: $0 start"
    fi
    ;;

  add-data)
    echo "Adding dummy data to database..."
    cd "$(dirname "$0")" || exit 1
    python backend/add_dummy_data.py
    ;;

  reset-data)
    echo -e "${YELLOW}⚠ This will clear all data and re-add dummy data${NC}"
    read -p "Continue? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
      cd "$(dirname "$0")" || exit 1
      python backend/add_dummy_data.py
      echo -e "${GREEN}✓${NC} Data reset complete"
    fi
    ;;

  test)
    echo "Running integration tests..."
    cd "$(dirname "$0")" || exit 1
    python backend/test_celery_integration.py
    ;;

  *)
    echo "Usage: $0 <command>"
    echo ""
    echo "Commands:"
    echo "  start       - Start Redis and Celery worker"
    echo "  stop        - Stop Redis and Celery worker"
    echo "  restart     - Restart services"
    echo "  status      - Show system status"
    echo "  logs        - View Celery logs (tail -f)"
    echo "  add-data    - Add dummy data to database"
    echo "  reset-data  - Clear and re-add dummy data"
    echo "  test        - Run integration tests"
    echo "  help        - Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 start"
    echo "  $0 logs"
    echo "  $0 status"
    ;;
esac
