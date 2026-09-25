# pyrefly: ignore [missing-import]
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Group(models.Model):
    name= models.CharField(max_length=100)
    created_by= models.ForeignKey(User, on_delete=models.CASCADE, related_name= 'created_groups')
    created_at= models.DateTimeField(auto_now_add=True)


class Membership(models.Model):
    ROLE_CHOICE=[('admin', 'Admin'), ('member', 'Member')]
    group= models.ForeignKey(Group, related_name="memberships", on_delete=models.CASCADE)
    user= models.ForeignKey(User, related_name='memberships', on_delete=models.CASCADE)
    role=models.CharField(max_length=10, choices=ROLE_CHOICE, default='member')
    joined_at= models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints=[
            models.UniqueConstraint(fields=['user', 'group'], name='unique_user_group_membership')
        ]