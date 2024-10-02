from rest_framework import generics, viewsets, mixins
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


class TasksCreateListViewsSet(mixins.ListModelMixin,
                              mixins.CreateModelMixin,
                              mixins.RetrieveModelMixin,
                              viewsets.GenericViewSet):
    queryset = Tasks.objects.all()
    serializer_class = TasksSerializer
