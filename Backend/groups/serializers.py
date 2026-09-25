from rest_framework import serializers
# pyrefly: ignore [missing-import]
from .models import Group

class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model=Group
        fields=['id', 'name', 'created_by', 'created_at']
        read_only_fields=['id','created_by', 'created_at']