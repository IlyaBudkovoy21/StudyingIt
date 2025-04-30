import json

from rest_framework import generics, viewsets, mixins
from rest_framework.permissions import IsAdminUser, AllowAny

from .services import return_task_by_one_cat, return_tasks_menu, return_many_cats, return_all_types, return_all_tasks
from .serializers import TasksSerializer, TasksMenuSerializer, AllTypes
from .models import Task, Type


class ListTasksByCat(generics.ListAPIView):
    """
    Class for view tasks by one category
    """

    serializer_class = TasksMenuSerializer
    lookup_url_kwarg = "cat"

    def get_queryset(self):
        cat = self.kwargs.get(self.lookup_url_kwarg)
        return return_task_by_one_cat(cat)


class TasksRetrieveListViewsSet(mixins.ListModelMixin,
                                mixins.RetrieveModelMixin,
                                viewsets.GenericViewSet):
    """
    View for menu of all tasks
    """

    queryset = return_tasks_menu()
    serializer_class = TasksMenuSerializer
    permission_classes = [AllowAny]


class FilterTasksByManyCats(generics.ListAPIView):
    serializer_class = TasksMenuSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        filter_param = self.request.GET.get("categories", None)
        return return_many_cats(filter_param)


class ReturnAllCategories(generics.ListAPIView):
    '''
    Return all categories
    '''

    serializer_class = AllTypes
    queryset = return_all_types()
