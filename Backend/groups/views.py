from rest_framework import permissions
# pyrefly: ignore [missing-import]
from .models import Group, Membership
# pyrefly: ignore [missing-import]
from .serializers import GroupSerializer
# pyrefly: ignore [missing-import]
from .permissions import IsGroupAdmin, IsGroupMember
from rest_framework import viewsets


class GroupViewSet(viewsets.ModelViewSet):
    queryset= Group.objects.all()
    serializer_class= GroupSerializer
    def perform_create(self, serializer):
        group= serializer.save(created_by= self.request.user)
        membership = Membership.objects.create(user=self.request.user, group=group, role='admin')
    def get_permissions(self):
        if self.action == 'update' or self.action =='partial_update':
            return [permissions.IsAuthenticated(), IsGroupAdmin()]
        elif self.action=='retrieve':
            return [permissions.IsAuthenticated(), IsGroupMember()]
        else:
            return [permissions.IsAuthenticated()]
