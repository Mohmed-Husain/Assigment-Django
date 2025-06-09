import os
import sys
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'employee_project.settings')
django.setup()

# Import management modules
from django.core.management import call_command

# Make migrations
print("Making migrations...")
call_command('makemigrations', 'employees')

# Apply migrations
print("\nApplying migrations...")
call_command('migrate')

print("\nMigrations completed successfully!")