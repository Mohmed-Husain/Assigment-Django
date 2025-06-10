# Employee Management System

A comprehensive Django REST API for managing employees, departments, attendance, and performance reviews.

## Features

- **Employee Management**: Create, read, update, and delete employee records
- **Department Management**: Organize employees by departments
- **Attendance Tracking**: Record and monitor employee attendance
- **Performance Reviews**: Manage employee performance evaluations
- **Data Visualization**: Visual representation of attendance and performance data
- **API Documentation**: Swagger/ReDoc documentation
- **Authentication**: Token-based authentication
- **Role-Based Access Control**: Different permission levels for admins, managers, and employees
- **Docker Support**: Easy deployment with Docker

## Tech Stack

- Django 5.1
- Django REST Framework
- PostgreSQL
- Swagger/ReDoc for API documentation
- Docker & Docker Compose

## Setup Instructions

### Prerequisites

- Python 3.9+
- PostgreSQL
- Docker (optional)

### Standard Setup

1. Clone the repository

2. Create a virtual environment and activate it
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file based on `.env.example` and configure your database settings

5. Run migrations
   ```bash
   python manage.py migrate
   ```

6. Seed the database with sample data (optional)
   ```bash
   python manage.py seed_data
   ```

7. Create a superuser
   ```bash
   python manage.py createsuperuser
   ```

8. Run the development server
   ```bash
   python manage.py runserver
   ```

### Docker Setup

1. Make sure Docker and Docker Compose are installed

2. Build and start the containers
   ```bash
   docker compose up --build
   ```

3. The application will be available at http://localhost:8000

4. To seed the database, set the `SEED_DATA=true` environment variable in the docker-compose.yml file or run:
   ```bash
   docker compose exec web python manage.py seed_data
   ```
   5. Alternatively, pull the pre-built image from Docker Hub:
      ```bash
      docker pull arkonafoob/assigmentdjango-web
      ```

## API Usage

### Authentication

1. Obtain an authentication token:
   ```bash
   curl -X POST http://localhost:8000/api-token-auth/ -d "username=your_username&password=your_password"
   ```

2. Use the token in subsequent requests:
   ```bash
   curl -H "Authorization: Token your_token_here" http://localhost:8000/api/employees/list/
   ```

### User Registration and Role Assignment

1. Register a new user:
   ```bash
   curl -X POST http://localhost:8000/api/employees/register/ \
     -H "Content-Type: application/json" \
     -d '{"username":"newuser", "password":"password123", "email":"user@example.com", "is_manager":false, "department":1}'
   ```

2. Admin users can promote users to managers by updating their profile:
   ```bash
   curl -X PATCH http://localhost:8000/api/employees/profiles/1/ \
     -H "Authorization: Token admin_token_here" \
     -H "Content-Type: application/json" \
     -d '{"is_manager":true}'
   ```

### Departments

- List all departments: `GET /api/employees/departments/`
- Create a department: `POST /api/employees/departments/`
- Get a specific department: `GET /api/employees/departments/{id}/`
- Update a department: `PUT /api/employees/departments/{id}/`
- Delete a department: `DELETE /api/employees/departments/{id}/`

### Employees

- List all employees: `GET /api/employees/list/`
- Create an employee: `POST /api/employees/list/`
- Get a specific employee: `GET /api/employees/list/{id}/`
- Update an employee: `PUT /api/employees/list/{id}/`
- Delete an employee: `DELETE /api/employees/list/{id}/`

### Attendance

- List all attendance records: `GET /api/attendance/`
- Create an attendance record: `POST /api/attendance/`
- Get a specific attendance record: `GET /api/attendance/{id}/`
- Update an attendance record: `PUT /api/attendance/{id}/`
- Delete an attendance record: `DELETE /api/attendance/{id}/`

### Performance

- List all performance records: `GET /api/performance/`
- Create a performance record: `POST /api/performance/`
- Get a specific performance record: `GET /api/performance/{id}/`
- Update a performance record: `PUT /api/performance/{id}/`
- Delete a performance record: `DELETE /api/performance/{id}/`

## Role-Based Access Control

The system implements three user roles with different permission levels:

1. **Admin Users**: Full access to all features and data
   - Can create, read, update, and delete all records
   - Can manage user roles and permissions

2. **Managers**: Limited administrative access
   - Can view all employee, attendance, and performance data
   - Can create and update attendance and performance records
   - Can update department information
   - Cannot delete employees or departments

3. **Employees**: Basic access to their own data
   - Can view their own profile, attendance, and performance records
   - Can view department information
   - Cannot modify any data

## Data Visualization

The system provides visual representations of attendance and performance data at `/api/employees/charts/`.

## Docker Support

See [README.docker.md](README.docker.md) for detailed instructions on using Docker with this project.

## Testing

Run the test suite with:

```bash
python manage.py test
```

## Deployment

This application can be deployed to various cloud platforms:

- **Render**: Follow the [Render deployment guide](https://render.com/docs/deploy-django)
- **Railway**: Follow the [Railway deployment guide](https://docs.railway.app/deploy/django)
- **Vercel**: Follow the [Vercel deployment guide](https://vercel.com/guides/deploying-django-to-vercel)

## License

This project is licensed under the MIT License.