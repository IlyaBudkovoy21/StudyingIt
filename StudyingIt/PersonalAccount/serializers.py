from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(ModelSerializer):

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        fields = ("username", "email", "password")
        model = User
