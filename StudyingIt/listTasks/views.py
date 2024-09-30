from rest_framework import generics, status
from rest_framework.response import Response

from .models import Tasks
from .serializers import TasksSerializer, AddTaskSerializer


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


class AddTask(generics.ListCreateAPIView):
    queryset = Tasks.objects.all()
    serializer_class = AddTaskSerializer

