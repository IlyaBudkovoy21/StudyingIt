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

    def create(self, request, *args, **kwargs):
        request.data['hash_name'] = sha224(request.data['name'].encode()).hexdigest()[:9]
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
