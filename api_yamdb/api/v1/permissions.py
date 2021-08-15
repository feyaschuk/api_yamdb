from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework.permissions import AllowAny

class IsModeratorOrAdminOrReadOnly(BasePermission):    
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            if (request.user.role=='admin' 
            or request.user.role=='moderator' or request.user.is_superuser):
                return True

class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or obj.author == request.user  
             

class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            if request.user.role=='admin' or request.user.is_superuser:
                return True
    

class IsAdminOrSuperUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'admin' or request.user.is_superuser

class CustomIsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated