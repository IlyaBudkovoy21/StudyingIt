from rest_framework import generics, status
from rest_framework.response import Response

from .models import Tasks
from .serializers import TasksSerializer


class ListTasksByCat(generics.ListAPIView):
    serializer_class = TasksSerializer

    def get_queryset(self):
        queryset = Tasks.objects.all()
        filter_param = self.kwargs['cat']
        queryset = queryset.filter(cat_id=filter_param)
        return queryset


class OneTask(generics.RetrieveAPIView):
    serializer_class = TasksSerializer
    lookup_url_kwarg = 'seq_num'
    queryset = Tasks.objects.all()


class AllTasks(generics.ListAPIView):
    serializer_class = TasksSerializer
    queryset = Tasks.objects.all()


class AddTask(generics.ListCreateAPIView):
    queryset = Tasks.objects.all()
    serializer_class = TasksSerializer
