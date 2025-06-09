from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Performance
from .serializers import PerformanceSerializer
from employee_project.permissions import IsAdminUser, IsManagerUser, IsEmployeeUser, IsOwnerOrAdmin

class PerformanceViewSet(viewsets.ModelViewSet):
    queryset = Performance.objects.all()
    serializer_class = PerformanceSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['employee', 'rating', 'review_date']
    ordering_fields = ['rating', 'review_date']
    
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
            
        return Performance.objects.none()
