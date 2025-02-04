from rest_framework import generics, viewsets, mixins
from rest_framework.permissions import IsAdminUser, AllowAny
from .models import Tasks
from .serializers import TasksSerializer, TasksMenuSerializer
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView

from .pagination_tasks import PaginTasks

import json


class ListTasksByCat(generics.ListAPIView):
    """
    Class for view tasks by one category
    """
    serializer_class = TasksMenuSerializer
    lookup_url_kwarg = "cat"

    def get_queryset(self):
        cat = self.kwargs.get(self.lookup_url_kwarg)
        return Tasks.tasks_menu.single_cat(cat)


class TasksRetrieveListViewsSet(mixins.ListModelMixin,
                                mixins.RetrieveModelMixin,
                                viewsets.GenericViewSet):
    """
    View for menu of all tasks
    """

    queryset = Tasks.tasks_menu.all()
    serializer_class = TasksMenuSerializer
    permission_classes = [AllowAny]


class CreateDestroyViewSet(mixins.CreateModelMixin,
                           mixins.DestroyModelMixin,
                           viewsets.GenericViewSet):
    queryset = Tasks.objects.all()
    serializer_class = TasksSerializer
    permission_classes = [IsAdminUser]


class FilterTasksByManyCats(generics.ListAPIView):
    serializer_class = TasksMenuSerializer
    permission_classes = [AllowAny]
    pagination_class = PaginTasks

    def get_queryset(self):
        filter_param = self.request.GET.get("categories", None)
        if not filter_param:
            return Tasks.tasks_menu.all()

        query = Q()
        filter_param = json.loads(filter_param)
        for cat in filter_param:
            query |= Q(cat_id=cat)
        return Tasks.tasks_menu.filter(query)
