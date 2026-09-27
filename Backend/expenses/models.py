from django.db.models import constraints
from django.db import models
from django.contrib.auth import get_user_model
from groups.models import Group

User=get_user_model()

class Expense(models.Model):
    SPLIT_CHOICES=[('equal','Equal'), ('exact','Exact'), ('percentage','Percentage')]
    amount= models.DecimalField(max_digits=10, decimal_places=3)
    description= models.TextField()
    paid_by=models.ForeignKey(User, on_delete=models.CASCADE, related_name='paid_expenses')
    split_type=models.CharField(max_length=10, choices=SPLIT_CHOICES, default='equal')
    group= models.ForeignKey(Group, on_delete=models.CASCADE, related_name='expenses')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=['-created_at']

    def __str__(self):
        return f"{self.description} - {self.amount}"

class ExpenseSplit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expense_splits')
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE, related_name='splits')
    share = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'expense'], name="unique_user_expense_split")
        ]

    def __str__(self):
        return f"{self.user}-{self.share}"