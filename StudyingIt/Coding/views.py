import os
from .s3 import client
import boto3
import botocore.exceptions
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from hashlib import sha224
import listTasks.models
import io
from rest_framework.parsers import JSONParser
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


class SaveCode(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        file = f'{request.data.get("username")}-test'
        try:
            client.upload_file(file, request.data.get("username"), request.data.get("code"))
            print("Файл загружен")
        except botocore.exceptions.NoCredentialsError:
            print("Ошибка отправки")
        return Response({"success": "Add code file"})