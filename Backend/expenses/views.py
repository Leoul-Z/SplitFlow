from rest_framework import permissions
from rest_framework import viewsets
from groups.permissions import IsGroupMember
# pyrefly: ignore [missing-import]
from .permissions import IsAllowedToEdit
# pyrefly: ignore [missing-import]
from .models import Expense
from django.contrib.auth import get_user_model
from rest_framework.response import Response
# pyrefly: ignore [missing-import]
from .serializers import ExpenseSerializer

User = get_user_model()

class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

    def perform_create(self, serializer):
        serializer.save(paid_by=self.request.user)

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsAllowedToEdit()]
        return [permissions.IsAuthenticated(), IsGroupMember()]