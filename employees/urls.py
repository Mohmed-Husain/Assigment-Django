from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DepartmentViewSet, EmployeeViewSet, UserProfileViewSet, ChartsView, register_user

router = DefaultRouter()
router.register(r'departments', DepartmentViewSet)
router.register(r'list', EmployeeViewSet)
router.register(r'profiles', UserProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('charts/', ChartsView.as_view(), name='charts'),
    path('register/', register_user, name='register'),
]