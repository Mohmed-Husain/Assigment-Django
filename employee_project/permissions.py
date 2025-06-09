from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    """
    Allows access only to admin users.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_staff

class IsManagerUser(permissions.BasePermission):
    """
    Allows access only to manager users.
    Manager users are identified by having the 'is_manager' flag in their user profile.
    """
    def has_permission(self, request, view):
        return bool(request.user and hasattr(request.user, 'profile') and 
                   request.user.profile.is_manager)

class IsEmployeeUser(permissions.BasePermission):
    """
    Allows access only to regular employee users.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object or admins to access it.
    Assumes the model instance has an `employee` attribute that is linked to a user.
    """
    def has_object_permission(self, request, view, obj):
        # Admin can see everything
        if request.user.is_staff:
            return True
            
        # Check if the object has an employee attribute and if it matches the request user
        if hasattr(obj, 'employee'):
            return obj.employee.user == request.user
        
        # For Employee model, check if the user is the employee
        if hasattr(obj, 'user'):
            return obj.user == request.user
            
        return False