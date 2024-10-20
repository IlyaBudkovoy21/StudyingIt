from rest_framework import serializers
from .models import Tasks, CodePatterns


class PatternSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodePatterns
        fields = "__all__"


class TasksSerializer(serializers.ModelSerializer):
    hash_name = serializers.SlugField(required=False)
    patterns = PatternSerializer()

    def create(self, validated_data):
        patt = validated_data.pop("patterns")
        a = CodePatterns.objects.create(**patt)
        task = Tasks.objects.create(**validated_data, patterns=a)
        return task

    class Meta:
        model = Tasks
        fields = "__all__"
