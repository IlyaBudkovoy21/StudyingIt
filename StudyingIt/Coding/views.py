import os

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
        client = boto3.client("s3", aws_access_key_id=os.getenv("ACCESS_KEY_AWS"),
                              aws_secret_access_key=os.getenv("ACCESS_KEY_AWS"),
                              region_name='ru-1')
        try:
            client.put_object(Bucket=os.getenv("BUCKET_NAME"), Key="client1/code1.txt", Body=request.data['code'])
            print("Файл загружен")
        except botocore.exceptions.NoCredentialsError:
            print("Ошибка отправки")
