import os, json
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
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import JSONParser
from listTasks.models import Tasks
import requests


class ReturnTask(generics.RetrieveAPIView):
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
            client.upload_file(file, request.data.get("username"), request.data.get("code"),
                               request.data.get("task_name"))
        except botocore.exceptions.NoCredentialsError:
            raise Exception("Ошибка отправки сообщения")
        cl = client.get_client()
        response = requests.post("http://localhost:1234/code", json={
            "path": f"{request.data.get("task_name")}-folder/{request.data.get("username")}-folder/{request.data.get("username")}-test",
            "lang": request.data.get("lang"),
            "task_name": request.data.get("task_name"),
            "username": request.data.get("username")})
        if response.status_code == 200:
            return Response({"correct": "Success data transfer"})
        else:
            return Response({"uncorrect": f"Unsuccess data transfer with status code -> {response.status_code}"})


@api_view(['GET'])
@permission_classes([AllowAny])
def get_user(request, access_token):
    jwt_auth = JWTAuthentication()
    try:
        validated_token = jwt_auth.get_validated_token(access_token)
        user = jwt_auth.get_user(validated_token)
        return Response({'username': str(user.username)})
    except TokenError as e:
        return Response({'detail': str(e)}, status=401)
    except Exception as e:
        return Response({'detail': str(e)}, status=500)

