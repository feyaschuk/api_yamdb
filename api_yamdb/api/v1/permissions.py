from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework.permissions import AllowAny

class IsModeratorOrAdminOrReadOnly(BasePermission):    
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            if request.method=="POST":
                return True
            elif (request.user.role=='admin' 
            or request.user.role=='moderator' or request.user.is_superuser):
                return True

    

class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        else:
            if request.method=="PATCH" or request.method=='DELETE':
                if obj.author == request.user:  
                    return True
             

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