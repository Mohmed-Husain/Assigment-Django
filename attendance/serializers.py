from rest_framework import serializers
from .models import Attendance

class AttendanceSerializer(serializers.ModelSerializer):
    employee_name = serializers.ReadOnlyField(source='employee.name')
    
    class Meta:
        model = Attendance
        fields = ['id', 'employee', 'employee_name', 'date', 'status', 'created_at', 'updated_at']