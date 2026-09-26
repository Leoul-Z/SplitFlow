from rest_framework import permissions
# pyrefly: ignore [missing-import]
from .models import Group, Membership
# pyrefly: ignore [missing-import]
from .serializers import GroupSerializer
# pyrefly: ignore [missing-import]
from .permissions import IsGroupAdmin, IsGroupMember
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model


User = get_user_model()

class GroupViewSet(viewsets.ModelViewSet):
    queryset= Group.objects.all()
    serializer_class= GroupSerializer
    def perform_create(self, serializer):
        group= serializer.save(created_by= self.request.user)
        membership = Membership.objects.create(user=self.request.user, group=group, role='admin', status='accepted')
    def get_permissions(self):
        if self.action == 'update' or self.action =='partial_update':
            return [permissions.IsAuthenticated(), IsGroupAdmin()]
        elif self.action=='retrieve' or self.action=='balance':
            return [permissions.IsAuthenticated(), IsGroupMember()]
        elif self.action == 'invite':
            return [permissions.IsAuthenticated(), IsGroupAdmin()]
        else:
            return [permissions.IsAuthenticated()]

    @action(detail=True, methods=['post'])
    def invite(self, request, pk=None):
        group= self.get_object()
        email = request.data.get('email')
        try:
            invited_user= User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'detail': 'No user with that email exists'}, status=404)
        if Membership.objects.filter(user=invited_user, group=group).exists():
            return Response({'detail', 'User is already a memeber or has a pending invite'}, status=400)
        Membership.objects.create(user=invited_user, group=group, status='pending', role='member')
        return Response({'detail': 'Invite sent'}, status=201)
    

    @action(detail=True, methods=['post'])
    def accept_invite(self, request, pk=None):
        user= request.user
        group= self.get_object()
        member=Membership.objects.filter(user=user, group=group, status='pending').update(status='accepted')
        if member:
            return Response({'detail':'Invite accepted'}, status=200)
        return Response({'detail':'No pending invite found'},status=400)

    @action(detail=True, methods=['get'])
    def balances(self, request, pk=None):
        group= self.get_object()
        memberships=Membership.objects.filter(group=group,status='accepted')

        data=[]
        for membership in memberships:
            data.append({
                'user_id':membership.user.id,
                'email':membership.user.email,
                'net_balance':0
            })
        return Response(data, status=200)