import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
from employees.models import Department, Employee
from attendance.models import Attendance
from performance.models import Performance

class Command(BaseCommand):
    help = 'Seeds the database with fake data'

    def handle(self, *args, **kwargs):
        fake = Faker()
        
        # Create departments
        self.stdout.write('Creating departments...')
        departments = [
            'Human Resources',
            'Engineering',
            'Finance',
            'Marketing',
            'Sales',
            'Customer Support',
            'Research & Development',
            'Legal',
            'Operations',
            'Product Management'
        ]
        
        department_objects = []
        for dept_name in departments:
            dept, created = Department.objects.get_or_create(name=dept_name)
            department_objects.append(dept)
            if created:
                self.stdout.write(f'Created department: {dept_name}')
        
        # Create employees
        self.stdout.write('Creating employees...')
        for i in range(50):  # Create 50 employees
            name = fake.name()
            email = fake.email()
            
            # Check if email already exists
            if Employee.objects.filter(email=email).exists():
                email = f"{name.replace(' ', '').lower()}_{random.randint(1, 999)}@{fake.domain_name()}"
            
            employee = Employee.objects.create(
                name=name,
                email=email,
                phone_number=fake.phone_number()[:15],
                address=fake.address(),
                date_of_joining=fake.date_between(start_date='-5y', end_date='today'),
                department=random.choice(department_objects)
            )
            self.stdout.write(f'Created employee: {employee.name}')
            
            # Create attendance records for the past 30 days
            self.stdout.write(f'Creating attendance records for {employee.name}...')
            for j in range(30):
                date = timezone.now().date() - timedelta(days=j)
                status_choices = ['present', 'absent', 'late']
                weights = [0.7, 0.1, 0.2]  # 70% present, 10% absent, 20% late
                status = random.choices(status_choices, weights=weights, k=1)[0]
                
                Attendance.objects.create(
                    employee=employee,
                    date=date,
                    status=status
                )
            
            # Create performance records (1-3 per employee)
            self.stdout.write(f'Creating performance records for {employee.name}...')
            
            # Get a list of unique review dates
            review_dates = []
            for k in range(random.randint(1, 3)):
                # Keep generating dates until we get a unique one
                while True:
                    review_date = fake.date_between(start_date=employee.date_of_joining, end_date='today')
                    if review_date not in review_dates:
                        review_dates.append(review_date)
                        break
                
                Performance.objects.create(
                    employee=employee,
                    rating=random.randint(1, 5),
                    review_date=review_date,
                    comments=fake.paragraph()
                )
        
        self.stdout.write(self.style.SUCCESS('Successfully seeded the database!'))