from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Department, Employee, UserProfile

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff']
        read_only_fields = ['is_staff']

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'is_manager', 'department', 'created_at', 'updated_at']

class EmployeeSerializer(serializers.ModelSerializer):
    department_name = serializers.ReadOnlyField(source='department.name')
    user_details = UserSerializer(source='user', read_only=True)
    
    class Meta:
        model = Employee
        fields = ['id', 'name', 'email', 'phone_number', 'address', 'position',
                 'department', 'department_name', 'date_of_joining', 
                 'created_at', 'updated_at', 'user', 'user_details']
        read_only_fields = ['date_of_joining', 'created_at', 'updated_at']