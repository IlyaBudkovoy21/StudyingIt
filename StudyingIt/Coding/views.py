from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from hashlib import sha224

import listTasks.models
from listTasks.models import Tasks


class ReturnTask(generics.RetrieveAPIView):
    serializer_class = listTasks.serializers.TasksSerializer

    def get_queryset(self):
        return Tasks.objects.all()

    def get_object(self):
        for i in self.get_queryset():
            a = i.name
            if sha224(a.encode()).hexdigest()[:9] == str(self.kwargs['name'])[:9]:
                return i
        raise ValueError("Unfound task")