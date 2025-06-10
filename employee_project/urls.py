"""
URL configuration for employee_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.authtoken.views import obtain_auth_token
from django.http import HttpResponse  # 👈 Add this

# 👇 Define a simple home view right here
def home(request):
    html = """
    <html>
    <head>
        <title>Employee Management API</title>
        <style>
            body { font-family: Arial; padding: 20px; }
            h1 { color: #2e6da4; }
            ul { line-height: 1.8em; }
        </style>
    </head>
    <body>
        <h1>Welcome to the Employee Management API</h1>
        <p>Available endpoints:</p>
        <ul>
            <li><a href="/swagger/">Swagger Docs</a></li>
            <li><a href="/redoc/">ReDoc Docs</a></li>
            <li><a href="/admin/">Admin Panel</a></li>
        </ul>
        
    </body>
    </html>
    """
    return HttpResponse(html)

#  <li><a href="/api-token-auth/">API Token Auth</a> (POST with username & password)</li>
            
#             <li><a href="/api/employees/departments/">Departments</a></li>
#             <li><a href="/api/employees/list/">Employees</a></li>
#             <li><a href="/api/employees/profiles/">User Profiles</a></li>
#             <li><a href="/api/employees/charts/">Charts</a></li>
#             <li><a href="/api/employees/register/">Register New User</a></li>

#             <li><a href="/api/attendance/">Attendance API Root</a></li>
#             <li><a href="/api/performance/">Performance API Root</a></li>
# <p><strong>Note:</strong> Some endpoints require POST/PUT methods or authentication and may not open directly in browser.</p>

schema_view = get_schema_view(
    openapi.Info(
        title="Employee Management API",
        default_version='v1',
        description="API for Employee Management System",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', home), 
    path('admin/', admin.site.urls),
    path('api/employees/', include('employees.urls')),
    path('api/attendance/', include('attendance.urls')),
    path('api/performance/', include('performance.urls')),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
