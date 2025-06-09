from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.utils import timezone
from employees.models import Department, Employee
from .models import Attendance
from .serializers import AttendanceSerializer


class AttendanceModelTest(TestCase):
    def setUp(self):
        self.department = Department.objects.create(name="Test Department")
        self.employee = Employee.objects.create(
            name="Test Employee",
            email="test@example.com",
            phone_number="1234567890",
            address="Test Address",
            department=self.department
        )
        self.attendance = Attendance.objects.create(
            employee=self.employee,
            date=timezone.now().date(),
            status="present"
        )

    def test_attendance_creation(self):
        self.assertEqual(self.attendance.employee, self.employee)
        self.assertEqual(self.attendance.status, "present")
        self.assertTrue(isinstance(self.attendance, Attendance))
        self.assertEqual(str(self.attendance), f"{self.employee.name} - {self.attendance.date} - present")


class AttendanceAPITest(TestCase):
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
        self.attendance_data = {
            'employee': self.employee.id,
            'date': self.today,
            'status': 'present'
        }
        
        self.attendance = Attendance.objects.create(
            employee=self.employee,
            date=self.today,
            status='present'
        )
        
        self.url = reverse('attendance-list')
        self.detail_url = reverse('attendance-detail', kwargs={'pk': self.attendance.pk})

    def test_create_attendance(self):
        # Create a new attendance for a different date
        new_data = self.attendance_data.copy()
        new_data['date'] = (self.today - timezone.timedelta(days=1)).isoformat()
        
        response = self.client.post(self.url, new_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Attendance.objects.count(), 2)

    def test_get_all_attendance(self):
        response = self.client.get(self.url)
        attendance_records = Attendance.objects.all()
        serializer = AttendanceSerializer(attendance_records, many=True)
        self.assertEqual(response.data['results'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_attendance(self):
        response = self.client.get(self.detail_url)
        attendance = Attendance.objects.get(pk=self.attendance.pk)
        serializer = AttendanceSerializer(attendance)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_attendance(self):
        updated_data = {
            'employee': self.employee.id,
            'date': self.today,
            'status': 'late'
        }
        response = self.client.put(self.detail_url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.attendance.refresh_from_db()
        self.assertEqual(self.attendance.status, 'late')

    def test_delete_attendance(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Attendance.objects.count(), 0)

    def test_filter_attendance_by_employee(self):
        url = f"{self.url}?employee={self.employee.id}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_filter_attendance_by_date(self):
        url = f"{self.url}?date={self.today}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_filter_attendance_by_status(self):
        url = f"{self.url}?status=present"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
