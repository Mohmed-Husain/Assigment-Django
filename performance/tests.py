from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.utils import timezone
from employees.models import Department, Employee
from .models import Performance
from .serializers import PerformanceSerializer


class PerformanceModelTest(TestCase):
    def setUp(self):
        self.department = Department.objects.create(name="Test Department")
        self.employee = Employee.objects.create(
            name="Test Employee",
            email="test@example.com",
            phone_number="1234567890",
            address="Test Address",
            department=self.department
        )
        self.performance = Performance.objects.create(
            employee=self.employee,
            review_date=timezone.now().date(),
            rating=4,
            comments="Good performance"
        )

    def test_performance_creation(self):
        self.assertEqual(self.performance.employee, self.employee)
        self.assertEqual(self.performance.rating, 4)
        self.assertEqual(self.performance.comments, "Good performance")
        self.assertTrue(isinstance(self.performance, Performance))
        self.assertEqual(str(self.performance), f"{self.employee.name} - {self.performance.review_date} - 4")


class PerformanceAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        
        self.department = Department.objects.create(name='Test Department')
        self.employee = Employee.objects.create(
            name='Test Employee',
            email='test@example.com',
            phone_number='1234567890',
            address='Test Address',
            department=self.department
        )
        
        self.today = timezone.now().date()
        self.performance_data = {
            'employee': self.employee.id,
            'review_date': self.today,
            'rating': 4,
            'comments': 'Good performance'
        }
        
        self.performance = Performance.objects.create(
            employee=self.employee,
            review_date=self.today,
            rating=4,
            comments='Good performance'
        )
        
        self.url = reverse('performance-list')
        self.detail_url = reverse('performance-detail', kwargs={'pk': self.performance.pk})

    def test_create_performance(self):
        # Create a new performance for a different date
        new_data = self.performance_data.copy()
        new_data['review_date'] = (self.today - timezone.timedelta(days=30)).isoformat()
        
        response = self.client.post(self.url, new_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Performance.objects.count(), 2)

    def test_get_all_performance(self):
        response = self.client.get(self.url)
        performance_records = Performance.objects.all()
        serializer = PerformanceSerializer(performance_records, many=True)
        self.assertEqual(response.data['results'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_performance(self):
        response = self.client.get(self.detail_url)
        performance = Performance.objects.get(pk=self.performance.pk)
        serializer = PerformanceSerializer(performance)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_performance(self):
        updated_data = {
            'employee': self.employee.id,
            'review_date': self.today,
            'rating': 5,
            'comments': 'Excellent performance'
        }
        response = self.client.put(self.detail_url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.performance.refresh_from_db()
        self.assertEqual(self.performance.rating, 5)
        self.assertEqual(self.performance.comments, 'Excellent performance')

    def test_delete_performance(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Performance.objects.count(), 0)

    def test_filter_performance_by_employee(self):
        url = f"{self.url}?employee={self.employee.id}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_filter_performance_by_rating(self):
        url = f"{self.url}?rating=4"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_filter_performance_by_review_date(self):
        url = f"{self.url}?review_date={self.today}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
