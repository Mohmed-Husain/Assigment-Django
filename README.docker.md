# Docker Setup for Django Employee Management System

This document provides instructions for running the Django Employee Management System using Docker.

## Prerequisites

- Docker
- Docker Compose

## Getting Started

### Build and Run the Application

1. Clone the repository (if you haven't already):

```bash
git clone <repository-url>
cd <repository-directory>
```

2. Build and start the containers:

```bash
docker-compose up --build
```

This will:
- Build the Docker image for the Django application
- Start the PostgreSQL database
- Apply migrations automatically
- Start the Django development server

3. Access the application at http://localhost:8000

### Seeding the Database

There are two ways to seed the database with sample data:

#### Option 1: Set SEED_DATA environment variable

In the `docker-compose.yml` file, set the `SEED_DATA` environment variable to `true`:

```yaml
web:
  # other settings...
  environment:
    # other environment variables...
    - SEED_DATA=true
```

Then restart the containers:

```bash
docker-compose down
docker-compose up
```

#### Option 2: Run the seed command manually

```bash
docker-compose exec web python manage.py seed_data
```

### Useful Commands

- Stop the containers:

```bash
docker-compose down
```

- View logs:

```bash
docker-compose logs
```

- Access the Django shell:

```bash
docker-compose exec web python manage.py shell
```

- Run migrations manually:

```bash
docker-compose exec web python manage.py migrate
```

- Create a superuser:

```bash
docker-compose exec web python manage.py createsuperuser
```

## Configuration

The Docker setup uses environment variables defined in the `docker-compose.yml` file. You can modify these variables as needed for your environment.

## Database

The PostgreSQL database data is persisted in a Docker volume named `postgres_data`. This ensures that your data is not lost when containers are stopped or removed.