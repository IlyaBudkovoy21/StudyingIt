from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from django.db.transaction import atomic
from django.core.exceptions import ObjectDoesNotExist

import requests
import logging
from .s3 import client
import botocore.exceptions
from datetime import datetime, timedelta

from listTasks.models import Tasks
from listTasks.serializers import TasksSerializer
from .permissions import NotForUsers
from PersonalAccount.models import DatesInfoUser
from PersonalAccount.utility import get_user_id_by_access
from django.contrib.auth.models import User

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
            return Response({"correct": "Success data transfer"}, status=status.HTTP_200_OK)
        else:
            log.error(f"{request.user}: Unsuccess data transfer")
            return Response({"uncorrect": f"Unsuccess data transfer with status code -> {response.status_code}"},
                            status=response.status_code)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_user(request, access_token):
    """
    Returns the user by the passed token
    """

    user = get_user_id_by_access(access_token)
    if user["status"] == "OK":
        return Response({'user_id': user["data"]}, status=status.HTTP_200_OK)
    return Response({'error': user["error"]}, status=status.HTTP_400_BAD_REQUEST)


class CodeMonitoring(APIView):
    """
    Class for save days of solving problems in a row
    """
    permission_classes = [NotForUsers]
    authentication_classes = []

    @staticmethod
    def get_or_create_info_user(id_user, user):
        try:
            return DatesInfoUser.objects.get(
                user__id=id_user)
        except ObjectDoesNotExist:
            return DatesInfoUser.objects.create(user=user)

    @staticmethod
    def get_user(user_id):
        try:
            return User.objects.get(id=user_id)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def get_task(task_id):
        try:
            return Tasks.objects.only("id", "name").get(id=task_id)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def update_user_streak(info_user):
        if info_user.day_start_row and info_user.day_start_row + timedelta(
                days=info_user.days_in_row + 1) == datetime.now().date():
            info_user.days_in_row += 1
            info_user.max_days = max(info_user.max_days, info_user.days_in_row)
        else:
            info_user.days_in_row = 0
            info_user.day_start_row = datetime.now().date()
        info_user.save()

    @atomic()
    def post(self, request):

        task_id = request.data.get("task_id", None)
        user_id = request.data.get("id", None)

        if not (all((task_id, user_id))):
            log.error("Not enough information to save")
            return Response("Not enough information to save", status=status.HTTP_400_BAD_REQUEST)

        user = CodeMonitoring.get_user(user_id)
        if user is None:
            log.error("User is not found")
            return Response("User is not found",
                            status=status.HTTP_400_BAD_REQUEST)

        info_user = CodeMonitoring.get_or_create_info_user(user_id, user)
        task = CodeMonitoring.get_task(task_id)

        if any(info is None for info in (info_user, task)):
            log.error("Some information about the user does not exist in the database")
            return Response("Some information about the user does not exist in the database",
                            status=status.HTTP_400_BAD_REQUEST)

        CodeMonitoring.update_user_streak(info_user)
        task.users_solved.add(user)

        return Response("Success data save", status=status.HTTP_200_OK)
