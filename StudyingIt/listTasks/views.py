from django.shortcuts import render
from rest_framework import generics

from .models import Tasks
from .serializers import TasksSerializer


class ListTasks(generics.ListAPIView):
    queryset = Tasks.objects.all()
    serializer_class = TasksSerializer
