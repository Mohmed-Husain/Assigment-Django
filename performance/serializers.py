from rest_framework import serializers
from .models import Performance

class PerformanceSerializer(serializers.ModelSerializer):
    employee_name = serializers.ReadOnlyField(source='employee.name')
    
    class Meta:
        model = Performance
        fields = ['id', 'employee', 'employee_name', 'rating', 'review_date', 'comments', 'created_at', 'updated_at']