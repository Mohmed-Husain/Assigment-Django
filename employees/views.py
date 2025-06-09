from rest_framework import viewsets, filters, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User
from .models import Department, Employee, UserProfile
from .serializers import DepartmentSerializer, EmployeeSerializer, UserProfileSerializer, UserSerializer
from employee_project.permissions import IsAdminUser, IsManagerUser, IsEmployeeUser, IsOwnerOrAdmin

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'created_at']
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser|IsManagerUser]
        else:
            permission_classes = [IsEmployeeUser]
        return [permission() for permission in permission_classes]

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['department', 'date_of_joining']
    search_fields = ['name', 'email']
    ordering_fields = ['name', 'date_of_joining', 'department__name']
    
    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            permission_classes = [IsAdminUser]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsAdminUser|IsManagerUser|IsOwnerOrAdmin]
        else:
            permission_classes = [IsEmployeeUser]
        return [permission() for permission in permission_classes]

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            permission_classes = [IsAdminUser]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsAdminUser|IsOwnerOrAdmin]
        else:
            permission_classes = [IsEmployeeUser]
        return [permission() for permission in permission_classes]
    
    @action(detail=False, methods=['get'])
    def my_profile(self, request):
        try:
            profile = UserProfile.objects.get(user=request.user)
            serializer = self.get_serializer(profile)
            return Response(serializer.data)
        except UserProfile.DoesNotExist:
            return Response({"detail": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    user_serializer = UserSerializer(data=request.data)
    if user_serializer.is_valid():
        user = user_serializer.save()
        user.set_password(request.data.get('password'))
        user.save()
        
        # Create user profile
        profile_data = {
            'user': user.id,
            'is_manager': request.data.get('is_manager', False),
            'department': request.data.get('department', None)
        }
        profile_serializer = UserProfileSerializer(data=profile_data)
        if profile_serializer.is_valid():
            profile_serializer.save()
            
            # Link to employee if email matches
            try:
                employee = Employee.objects.get(email=user.email)
                employee.user = user
                employee.save()
            except Employee.DoesNotExist:
                pass
                
            return Response({
                'user': user_serializer.data,
                'profile': profile_serializer.data
            }, status=status.HTTP_201_CREATED)
        else:
            user.delete()
            return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Add this to the existing views.py file
from django.views.generic import TemplateView

class ChartsView(TemplateView):
    template_name = 'charts.html'
