from rest_framework.decorators import permission_classes
from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework.permissions import AllowAny

class IsOwnerOrModeratorOrReadOnly(BasePermission):    
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if obj.author == request.user or request.user.role=='moderator'or request.user.role=='admin':
            return True


              

