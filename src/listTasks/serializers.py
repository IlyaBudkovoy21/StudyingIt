from hashlib import sha224

from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Task, ExamplesForTask, Type




class PatternSerializer(serializers.ModelSerializer):
    """
    Serializer for patterns
    """

    class Meta:
        model = ExamplesForTask
        fields = "__all__"


class TypeSerializer(serializers.ModelSerializer):
    """
    Serializer for patterns
    """

    class Meta:
        model = Type
        fields = "__all__"


class TasksSerializer(serializers.ModelSerializer):
    """
    Serializer for tasks
    """
    patterns = PatternSerializer()
    cat = TypeSerializer()
    users_solved = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.all(),
        required=False,  # Разрешает отсутствие поля в запросе
        allow_empty=True,  # Разрешает пустой список []
    )

    def create(self, validated_data):
        patt = validated_data.pop("patterns")
        validated_data['hash_name'] = sha224(validated_data['name'].encode()).hexdigest()[:9]
        a = ExamplesForTask.objects.create(**patt)
        task = Task.objects.create(**validated_data, patterns=a)
        return task

    class Meta:
        model = Task
        fields = "__all__"


class TasksMenuSerializer(serializers.ModelSerializer):
    """
    Serializer for tasks for menu
    """

    class Meta:
        model = Task
        fields = ["id", "name", "hash_name", "cost", "cat_id"]


class AllTypes(serializers.ModelSerializer):
    '''
    Serializer for types
    '''

    class Meta:
        fields = '__all__'
        model = Type
