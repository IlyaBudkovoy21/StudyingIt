from rest_framework import generics, viewsets, mixins
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from .models import Tasks
from .serializers import TasksSerializer


class ListTasksByCat(generics.ListAPIView):
    serializer_class = TasksSerializer

    def get_queryset(self):
        queryset = Tasks.objects.all()
        filter_param = self.kwargs['cat']
        queryset = queryset.filter(cat_id=filter_param)
        return queryset


class TasksRetrieveListViewsSet(mixins.ListModelMixin,
                                mixins.RetrieveModelMixin,
                                viewsets.GenericViewSet):
    queryset = Tasks.objects.all()
    serializer_class = TasksSerializer
    permission_classes = [AllowAny]


class CreateDestroyViewSet(mixins.CreateModelMixin,
                           mixins.DestroyModelMixin,
                           viewsets.GenericViewSet):
    queryset = Tasks.objects.all()
    serializer_class = TasksSerializer
    permission_classes = [IsAdminUser]
