from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Attendance
from .serializers import AttendanceSerializer
from employee_project.permissions import IsAdminUser, IsManagerUser, IsEmployeeUser, IsOwnerOrAdmin

class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['employee', 'date', 'status']
    ordering_fields = ['date', 'status']
    
    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            permission_classes = [IsAdminUser|IsManagerUser]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsAdminUser|IsManagerUser]
        else:
            permission_classes = [IsEmployeeUser]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        
        # If user is admin or manager, return all records
        if user.is_staff or (hasattr(user, 'profile') and user.profile.is_manager):
            return queryset
            
        # For regular employees, only return their own records
        if hasattr(user, 'employee'):
            return queryset.filter(employee=user.employee)
            
        return Attendance.objects.none()

    