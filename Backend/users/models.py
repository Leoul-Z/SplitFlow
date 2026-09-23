from enum import unique
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email= models.EmailField(unique=True)
    avatar_color= models.CharField(max_length=7, default='#46F5E5')

    USERNAME_FIELD="email"
    REQUIRED_FIELDS=["username"]

    def __str__(self):
        return self.email
