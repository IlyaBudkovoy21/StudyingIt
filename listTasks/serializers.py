from rest_framework import serializers

from .models import Tasks, CodePatterns, Types

from hashlib import sha224



class PatternSerializer(serializers.ModelSerializer):
    """
    Serializer for patterns
    """

    class Meta:
        model = CodePatterns
        fields = "__all__"


class TasksSerializer(serializers.ModelSerializer):
    """
    Serializer for tasks
    """
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


class TasksMenuSerializer(serializers.ModelSerializer):
    """
    Serializer for tasks for menu
    """

    class Meta:
        model = Tasks
        fields = ["id", "name", "hash_name", "cost", "cat_id"]


class AllTypes(serializers.ModelSerializer):
    '''
    Serializer for types
    '''

    class Meta:
        fields = '__all__'
        model = Types
