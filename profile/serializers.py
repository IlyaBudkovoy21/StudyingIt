from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.contrib.auth.models import User
from django.db import transaction
from django.db.utils import IntegrityError

from .models import DatesInfoUser


class UserSerializer(ModelSerializer):

    username = serializers.CharField()
    password = serializers.CharField()
    email = serializers.EmailField()

    @transaction.atomic()
    def create(self, validated_data):
        try:
            user = User(
                username=validated_data['username'],
                email=validated_data['email']
            )
            user.set_password(validated_data['password'])
            user.save()
            DatesInfoUser.objects.create(user=user)
            return user
        except KeyError:
            raise serializers.ValidationError("Not enough info to create user")
        except IntegrityError:
            raise serializers.ValidationError(f"User with username {validated_data['username']} already exists")

    class Meta:
        fields = ("username", "email", "password")
        model = User



class ProfileSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=20)
    max_days = serializers.IntegerField()
    current_days_row = serializers.IntegerField()
    tasks = serializers.ListSerializer(child=serializers.DictField())


class TokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField()