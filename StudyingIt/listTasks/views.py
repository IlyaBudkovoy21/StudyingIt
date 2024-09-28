from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from .models import Tasks
from .serializers import TasksSerializer


class ListTasks(generics.ListAPIView):
    serializer_class = TasksSerializer

    def get_queryset(self):
        return Tasks.objects.filter(cat_id=self.kwargs.get('cat'))


