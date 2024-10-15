from rest_framework import serializers

from .models import Tasks


class TasksSerializer(serializers.ModelSerializer):
    hash_name = serializers.SlugField()

    class Meta:
        model = Tasks
        fields = "__all__"
