from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User


class UserRegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField()

    def validate_username(self, username):
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise ValidationError('This username busy!')