from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from .models import Tasks
from .serializers import TasksSerializer
from django.db.models import Q


class ListTasksByCat(generics.ListAPIView):
    serializer_class = TasksSerializer

    def get_queryset(self):
        return Tasks.objects.filter(cat_id=self.kwargs.get('cat'))


class AllTasks(generics.ListAPIView):
    serializer_class = TasksSerializer

    def get_queryset(self):
        return Tasks.objects.all()


class OneTask(generics.RetrieveAPIView):
    serializer_class = TasksSerializer
    lookup_url_kwarg = 'seq_num'

    def get_queryset(self):
        return Tasks.objects.all()
