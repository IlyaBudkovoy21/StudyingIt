from rest_framework import generics, viewsets, mixins
from rest_framework.permissions import IsAdminUser, AllowAny
from .models import Tasks
from .serializers import TasksSerializer, TasksMenuSerializer
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView


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


class FilterTasksByManyCats(APIView):
    serializer_class = TasksMenuSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        filter_param = request.data.get("cat")
        if not filter_param:
            filtered_queryset = Tasks.tasks_menu.all()
            serializer = self.serializer_class(filtered_queryset, many=True)
            return Response(serializer.data)

        query = Q()
        for cat in filter_param:
            query |= Q(cat_id=cat)

        filtered_queryset = Tasks.tasks_menu.filter(query)
        serializer = self.serializer_class(filtered_queryset, many=True)
        return Response(serializer.data)
