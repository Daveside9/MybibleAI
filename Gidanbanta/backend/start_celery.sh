#!/bin/bash

echo "Starting Celery Worker with Beat Scheduler..."
echo ""
echo "Make sure Redis is running on localhost:6379"
echo ""

# Get the directory of this script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

# Activate virtual environment if it exists
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
fi

# Start Celery worker with beat
python run_celery.py
