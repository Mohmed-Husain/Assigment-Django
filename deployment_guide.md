# Deployment Guide

This guide provides instructions for deploying the Employee Management System to various cloud platforms.

## Deploying to Render

[Render](https://render.com/) is a unified cloud platform that offers free web services with SSL, a global CDN, private networks, and auto deploys from Git.

### Prerequisites

- A Render account
- Your project code in a Git repository (GitHub, GitLab, etc.)

### Steps

1. **Create a PostgreSQL Database**

   - Log in to your Render dashboard
   - Click on "New" and select "PostgreSQL"
   - Configure your database:
     - Name: `employee-management-db` (or your preferred name)
     - Database: `employee_management`
     - User: Render will generate this for you
     - Choose a region close to your users
     - Select a plan (Free tier is available)
   - Click "Create Database"
   - Once created, note the following information:
     - Internal Database URL
     - External Database URL
     - Database Name
     - Username
     - Password

2. **Create a Web Service**

   - Click on "New" and select "Web Service"
   - Connect your Git repository
   - Configure your web service:
     - Name: `employee-management-system` (or your preferred name)
     - Runtime: Python
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `gunicorn employee_project.wsgi:application`
     - Choose a plan (Free tier is available)
   - Add the following environment variables:
     - `DATABASE_URL`: Use the External Database URL from your PostgreSQL service
     - `SECRET_KEY`: Generate a secure random string
     - `DEBUG`: Set to `False` for production
     - `ALLOWED_HOSTS`: Add your Render domain (e.g., `employee-management-system.onrender.com`)
   - Click "Create Web Service"

3. **Run Migrations and Seed Data**

   - Once your service is deployed, go to the "Shell" tab
   - Run the following commands:
     ```bash
     python manage.py migrate
     python manage.py seed_data  # Optional
     python manage.py createsuperuser
     ```

4. **Access Your Application**

   - Your application will be available at the URL provided by Render (e.g., `https://employee-management-system.onrender.com`)

## Deploying to Railway

[Railway](https://railway.app/) is a deployment platform that allows you to deploy your code with zero configuration.

### Prerequisites

- A Railway account
- Your project code in a Git repository

### Steps

1. **Create a New Project**

   - Log in to your Railway dashboard
   - Click on "New Project"
   - Select "Deploy from GitHub repo"
   - Connect your GitHub account and select your repository

2. **Add a PostgreSQL Database**

   - In your project dashboard, click on "+ New"
   - Select "Database" and then "PostgreSQL"
   - Railway will automatically provision a PostgreSQL database

3. **Configure Environment Variables**

   - Go to the "Variables" tab in your project
   - Add the following variables:
     - `DATABASE_URL`: Railway will automatically inject this
     - `SECRET_KEY`: Generate a secure random string
     - `DEBUG`: Set to `False` for production
     - `ALLOWED_HOSTS`: Add your Railway domain

4. **Configure the Build and Start Commands**

   - Go to the "Settings" tab in your service
   - Set the build command: `pip install -r requirements.txt`
   - Set the start command: `gunicorn employee_project.wsgi:application`

5. **Run Migrations and Seed Data**

   - Click on your service and go to the "Shell" tab
   - Run the following commands:
     ```bash
     python manage.py migrate
     python manage.py seed_data  # Optional
     python manage.py createsuperuser
     ```

6. **Access Your Application**

   - Your application will be available at the URL provided by Railway

## Deploying to Vercel

[Vercel](https://vercel.com/) is a cloud platform for static sites and serverless functions.

### Prerequisites

- A Vercel account
- Your project code in a Git repository
- A PostgreSQL database (can be hosted elsewhere like Render or Railway)

### Steps

1. **Create a `vercel.json` File**

   Create a `vercel.json` file in the root of your project with the following content:

   ```json
   {
     "builds": [
       {
         "src": "employee_project/wsgi.py",
         "use": "@vercel/python"
       }
     ],
     "routes": [
       {
         "src": "/(.*)",
         "dest": "employee_project/wsgi.py"
       }
     ]
   }
   ```

2. **Create a `wsgi.py` File for Vercel**

   Update your `employee_project/wsgi.py` file to include the Vercel handler:

   ```python
   import os
   from django.core.wsgi import get_wsgi_application

   os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'employee_project.settings')
   application = get_wsgi_application()
   app = application
   ```

3. **Deploy to Vercel**

   - Install the Vercel CLI: `npm i -g vercel`
   - Run `vercel` in your project directory
   - Follow the prompts to link your project to Vercel
   - Set the environment variables:
     - `DATABASE_URL`: Your PostgreSQL database URL
     - `SECRET_KEY`: Generate a secure random string
     - `DEBUG`: Set to `False` for production
     - `ALLOWED_HOSTS`: Add your Vercel domain

4. **Run Migrations and Seed Data**

   Since Vercel doesn't provide a shell, you'll need to run migrations locally or on another platform:

   ```bash
   # Set your environment variables to match the production environment
   export DATABASE_URL="your_production_database_url"
   python manage.py migrate
   python manage.py seed_data  # Optional
   python manage.py createsuperuser
   ```

5. **Access Your Application**

   - Your application will be available at the URL provided by Vercel

## Additional Considerations for Production

1. **Static Files**

   For production, you should configure static file serving using a service like AWS S3 or Cloudinary. Update your settings.py accordingly.

2. **Security**

   - Ensure `DEBUG` is set to `False`
   - Use a strong, unique `SECRET_KEY`
   - Configure `ALLOWED_HOSTS` properly
   - Consider adding HTTPS redirect

3. **Performance**

   - Consider adding caching
   - Use a production-ready web server like Gunicorn
   - Configure database connection pooling

4. **Monitoring**

   - Set up logging
   - Consider using a monitoring service like Sentry

5. **Backups**

   - Set up regular database backups