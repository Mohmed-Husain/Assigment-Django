from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AttendanceViewSet

router = DefaultRouter()
router.register('attendances', AttendanceViewSet)

urlpatterns = [
    path('', include(router.urls)),
]