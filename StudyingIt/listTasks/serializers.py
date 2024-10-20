from rest_framework import serializers
from .models import Tasks, CodePatterns


class PatternSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodePatterns
        fields = "__all__"


class TasksSerializer(serializers.ModelSerializer):
    hash_name = serializers.SlugField(required=False)
    patterns = PatternSerializer()

    class Meta:
        model = Tasks
        fields = "__all__"
