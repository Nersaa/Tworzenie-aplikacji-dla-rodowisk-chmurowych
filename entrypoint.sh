#!/bin/sh

set -e

echo "Waiting for database to be ready..."
sleep 5

echo "Initializing database..."
python init_db.py

echo "Adding test data..."
python add_test_data.py

echo "Starting Flask application..."
flask run --host=0.0.0.0

