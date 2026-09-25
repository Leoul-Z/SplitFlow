from rest_framework import permissions
# pyrefly: ignore [missing-import]
from .models import Membership

class IsGroupMember(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return Membership.objects.filter(user=request.user, group=obj).exists()

class IsGroupAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return Membership.objects.filter(user=request.user, group=obj, role='admin').exists()
        