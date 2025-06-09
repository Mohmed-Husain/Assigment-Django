#!/bin/bash

# Wait for postgres to be ready
echo "Waiting for PostgreSQL..."
sleep 5

# Apply database migrations
echo "Applying migrations..."
python manage.py migrate

# Seed data if specified
if [ "$SEED_DATA" = "true" ]; then
    echo "Seeding database..."
    python manage.py seed_data
fi

# Start server
echo "Starting server..."
exec "$@"