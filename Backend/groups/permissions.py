from rest_framework import permissions
# pyrefly: ignore [missing-import]
from .models import Membership, Group

class IsGroupMember(permissions.BasePermission):
    def get_group(self, obj):
        return obj if isinstance(obj, Group) else obj.group

    def has_object_permission(self, request, view, obj):
        return Membership.objects.filter(user=request.user, group=obj, status='accepted').exists()

class IsGroupAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return Membership.objects.filter(user=request.user, group=obj, status='accepted' ,role='admin').exists()


