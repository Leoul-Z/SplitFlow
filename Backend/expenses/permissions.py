from rest_framework import permissions

class IsAllowedToEdit(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.paid_by == request.user