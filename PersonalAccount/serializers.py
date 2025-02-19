from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.contrib.auth.models import User
from django.db import transaction

from .models import DatesInfoUser


class UserSerializer(ModelSerializer):
    @transaction.atomic()
    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        DatesInfoUser.objects.create(user=user)
        return user

    class Meta:
        fields = ("username", "email", "password")
        model = User


class ProfileSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=20)
    max_days = serializers.IntegerField()
    current_days_row = serializers.IntegerField()
    tasks = serializers.ListSerializer(child=serializers.IntegerField())