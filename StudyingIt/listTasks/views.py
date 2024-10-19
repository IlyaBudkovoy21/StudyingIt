from rest_framework import generics, viewsets, mixins
from rest_framework.permissions import IsAdminUser, AllowAny
from .models import Tasks
from rest_framework import status
from rest_framework.response import Response
from .serializers import TasksSerializer
from hashlib import sha224


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

    def perform_create(self, serializer):
        serializer.validated_data['hash_name'] = sha224(serializer.validated_data['name'].encode()).hexdigest()[:9]
        serializer.save()
