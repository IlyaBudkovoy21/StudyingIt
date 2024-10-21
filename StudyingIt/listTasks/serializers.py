from rest_framework import serializers
from .models import Tasks, CodePatterns
from hashlib import sha224


class PatternSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodePatterns
        fields = "__all__"


class TasksSerializer(serializers.ModelSerializer):
    patterns = PatternSerializer()

    def create(self, validated_data):
        patt = validated_data.pop("patterns")
        validated_data['hash_name'] = sha224(validated_data['name'].encode()).hexdigest()[:9]
        a = CodePatterns.objects.create(**patt)
        task = Tasks.objects.create(**validated_data, patterns=a)
        return task

    class Meta:
        model = Tasks
        fields = "__all__"
