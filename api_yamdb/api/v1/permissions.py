from rest_framework.decorators import permission_classes
from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework.permissions import AllowAny

class IsOwnerOrModeratorOrReadOnly(BasePermission):    
    def has_object_permission(self, request, view, obj):
        if request.method not in SAFE_METHODS:
            if (obj.author == request.user 
                or request.user.role=='moderator'
                or request.user.role=='admin'):
                return True

class IsOwnerOrModeratorOrAdmin(BasePermission):    
    def has_object_permission(self, request, view, obj):
        if (obj.author == request.user 
            or request.user.role=='moderator'
            or request.user.role=='admin'):
            return True

class IsAdminOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser

class IsModeratorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or request.user.role=='moderator'             

class IsAdminOrSuperUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'admin' or request.user.is_superuser

class CustomIsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated
