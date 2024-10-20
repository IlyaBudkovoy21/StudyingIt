import os
from .s3 import client
import boto3
from rest_framework import mixins
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
import requests


class ReturnTask(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = listTasks.serializers.TasksSerializer

    def get_queryset(self):
        return Tasks.objects.all()

    def get_object(self):
        for i in self.get_queryset():
            if i.hash_name == self.kwargs["name"]:
                return i


class SaveCode(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        file = f'{request.data.get("username")}-test'
        try:
            client.upload_file(file, request.data.get("username"), request.data.get("code"))
            print("Файл загружен")
        except botocore.exceptions.NoCredentialsError:
            print("Ошибка отправки")
        cl = client.get_client()
        url = cl.generate_presigned_url(
            'get_object',
            ExpiresIn=2592000,
            Params={"Bucket": os.getenv("BUCKET_NAME"),
                    "Key": file}
        )
        response = requests.post("http://localhost:1234/code", data={"link": url,
                                                                     "lang": request.data.lang,
                                                                     "task_name": request.data.name_task})
        if response.status_code == 200:
            return Responce({"correct": "Success data transfer"})
        else:
            return Responce({"uncorrect": f"Unsuccess data transfer with status code -> {response.status_code}"})
