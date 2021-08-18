from rest_framework.permissions import SAFE_METHODS, BasePermission


# class IsModeratorOrAdminOrReadOnly(BasePermission):
#     def has_permission(self, request, view):
#         if request.user.is_authenticated:
#             if (
#                     request.method == 'POST'
#                     or request.method == 'PATCH'
#                     or request.method == 'DELETE'
#             ):
#                 return True
#             elif (
#                     request.user.role == 'admin'
#                     or request.user.role == 'moderator'
#                     or request.user.is_superuser
#             ):
#                 return True
#         return request.method in SAFE_METHODS
#
#
# class IsOwnerOrModeratorOrAdminOrReadOnly(BasePermission):
#     def has_object_permission(self, request, view, obj):
#         if request.method == 'PATCH' or request.method == 'DELETE':
#             if obj.author == request.user or (
#                     request.user.role == 'admin'
#                     or request.user.role == 'moderator'
#                     or request.user.is_superuser
#             ):
#                 return True
#         return request.method in SAFE_METHODS
#
#
# class IsAdminOrReadOnly(BasePermission):
#     def has_permission(self, request, view):
#         if request.user.is_authenticated:
#             if request.user.role == 'admin' or request.user.is_superuser:
#                 return True
#         return request.method in SAFE_METHODS

class IsNotSafeMethod(BasePermission):
    def has_permission(self, request, view):
        return request.method not in SAFE_METHODS


class IsSafeMethod(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class IsModerator(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'moderator'


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'admin'


class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser


class CustomIsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated
