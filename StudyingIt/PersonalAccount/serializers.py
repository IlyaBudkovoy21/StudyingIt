from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User


class UserSerializer(ModelSerializer):
    class Meta:
        field = ("username", "first_name", "last_name", "email", "password")
        model = User
