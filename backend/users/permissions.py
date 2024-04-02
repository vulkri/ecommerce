from rest_framework import permissions


class IsManager(permissions.BasePermission):

    def has_permission(self, request, view):
        if 'manager' in request.user.groups.values_list("name", flat=True):
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if 'manager' in request.user.groups.values_list("name", flat=True):
            return True
        return False
    

class IsClient(permissions.BasePermission):

    def has_permission(self, request, view):
        if 'client' in request.user.groups.values_list("name", flat=True):
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if 'client' in request.user.groups.values_list("name", flat=True):
            return True
        return False