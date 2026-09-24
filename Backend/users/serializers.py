from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password as django_validate_password
from django.core.exceptions import ValidationError


User=get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model= User
        fields= ['id','username','email','avatar_color' ]
        read_only_fields=['id','email']

class RegisterSerializer(serializers.ModelSerializer):
    password= serializers.CharField(write_only=True, required=True, min_length=8)

    def validate_password(self, value):
        try:
            django_validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(list(e.messages))
        return value


    class Meta:
        model= User
        fields= ['id','username','email', 'password' ,'avatar_color' ]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
