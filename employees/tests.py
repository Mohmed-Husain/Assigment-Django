from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .models import Department, Employee
from .serializers import DepartmentSerializer, EmployeeSerializer


class DepartmentModelTest(TestCase):
    def setUp(self):
        self.department = Department.objects.create(name="Test Department")

    def test_department_creation(self):
        self.assertEqual(self.department.name, "Test Department")
        self.assertTrue(isinstance(self.department, Department))
        self.assertEqual(str(self.department), "Test Department")


class EmployeeModelTest(TestCase):
    def setUp(self):
        self.department = Department.objects.create(name="Test Department")
        self.employee = Employee.objects.create(
            name="Test Employee",
            email="test@example.com",
            phone_number="1234567890",
            address="Test Address",
            department=self.department
        )

    def test_employee_creation(self):
        self.assertEqual(self.employee.name, "Test Employee")
        self.assertEqual(self.employee.email, "test@example.com")
        self.assertEqual(self.employee.phone_number, "1234567890")
        self.assertEqual(self.employee.address, "Test Address")
        self.assertEqual(self.employee.department, self.department)
        self.assertTrue(isinstance(self.employee, Employee))
        self.assertEqual(str(self.employee), "Test Employee")


class DepartmentAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        
        self.department_data = {'name': 'Test Department'}
        self.department = Department.objects.create(name='Existing Department')
        self.url = reverse('department-list')
        self.detail_url = reverse('department-detail', kwargs={'pk': self.department.pk})

    def test_create_department(self):
        response = self.client.post(self.url, self.department_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Department.objects.count(), 2)

    def test_get_all_departments(self):
        response = self.client.get(self.url)
        departments = Department.objects.all()
        serializer = DepartmentSerializer(departments, many=True)
        self.assertEqual(response.data['results'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_department(self):
        response = self.client.get(self.detail_url)
        department = Department.objects.get(pk=self.department.pk)
        serializer = DepartmentSerializer(department)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_department(self):
        updated_data = {'name': 'Updated Department'}
        response = self.client.put(self.detail_url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.department.refresh_from_db()
        self.assertEqual(self.department.name, 'Updated Department')

    def test_delete_department(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Department.objects.count(), 0)


class EmployeeAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        
        self.department = Department.objects.create(name='Test Department')
        self.employee_data = {
            'name': 'Test Employee',
            'email': 'test@example.com',
            'phone_number': '1234567890',
            'address': 'Test Address',
            'department': self.department.id
        }
        self.employee = Employee.objects.create(
            name='Existing Employee',
            email='existing@example.com',
            phone_number='0987654321',
            address='Existing Address',
            department=self.department
        )
        self.url = reverse('employee-list')
        self.detail_url = reverse('employee-detail', kwargs={'pk': self.employee.pk})

    def test_create_employee(self):
        response = self.client.post(self.url, self.employee_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Employee.objects.count(), 2)

    def test_get_all_employees(self):
        response = self.client.get(self.url)
        employees = Employee.objects.all()
        serializer = EmployeeSerializer(employees, many=True)
        self.assertEqual(response.data['results'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_employee(self):
        response = self.client.get(self.detail_url)
        employee = Employee.objects.get(pk=self.employee.pk)
        serializer = EmployeeSerializer(employee)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_employee(self):
        updated_data = {
            'name': 'Updated Employee',
            'email': 'updated@example.com',
            'phone_number': '5555555555',
            'address': 'Updated Address',
            'department': self.department.id
        }
        response = self.client.put(self.detail_url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.employee.refresh_from_db()
        self.assertEqual(self.employee.name, 'Updated Employee')
        self.assertEqual(self.employee.email, 'updated@example.com')

    def test_delete_employee(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Employee.objects.count(), 0)
