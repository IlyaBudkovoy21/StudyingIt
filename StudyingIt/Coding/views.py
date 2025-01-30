from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view, permission_classes
from django.db.transaction import atomic
from django.shortcuts import get_object_or_404

import requests, logging
from .s3 import client
import botocore.exceptions
from datetime import datetime, timedelta

from listTasks.models import Tasks
from listTasks.serializers import TasksSerializer
from .permissions import NotForUsers
from PersonalAccount.models import DatesInfoUser

log = logging.getLogger("Coding.views")


class ReturnTask(generics.RetrieveAPIView):
    """
    View for return one task to solving
    """

    serializer_class = TasksSerializer

    def get_queryset(self):
        return Tasks.objects.all()

    def get_object(self):
        return self.get_queryset().get(hash_name=self.kwargs["name"])


class SaveCode(APIView):
    """
    View to save solutions
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        file = f'{request.data.get("username")}-test'
        try:
            client.upload_file(file, request.data.get("username"), request.data.get("code"),
                               request.data.get("task_name"))
        except botocore.exceptions.NoCredentialsError:
            log.error(f"Ошибка отправки сообщения в S3 для пользователя {request.data.get("username")}")
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
            log.error(f"{request.user}: Unsuccess data transfer")
            return Response({"uncorrect": f"Unsuccess data transfer with status code -> {response.status_code}"})


@api_view(['GET'])
@permission_classes([AllowAny])
def get_user(request, access_token):
    """
    Returns the user by the passed token
    """
    jwt_auth = JWTAuthentication()
    try:
        validated_token = jwt_auth.get_validated_token(access_token)
        user = jwt_auth.get_user(validated_token)
        return Response({'username': str(user.username)}, status=200)
    except Exception as e:
        log.error("Invalid token")
        return Response({'error': str(e)}, status=400)


class CodeMonitoring(APIView):
    """
    Class for save days of solving problems in a row
    """
    permission_classes = [NotForUsers]

    @atomic()
    def patch(self, request, **kwargs):
        try:
            info_user = DatesInfoUser.objects.get(
                user__username=kwargs["username"])
            if info_user.day_start_row + timedelta(
                    days=info_user.days_in_row + 1) == datetime.now().date():
                info_user.days_in_row += 1
                info_user.max_days = max(info_user.max_days, info_user.days_in_row)
            else:
                info_user.days_in_row = 0
                info_user.day_start_row = datetime.now().date()
            info_user.save()
            return Response("Success date save", status=200)
        except Exception as e:
            # place for logger
            return Response(f"Unsuccess date save: {e}", status=507)
