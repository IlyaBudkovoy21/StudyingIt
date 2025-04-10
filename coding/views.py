import requests
import logging
from .s3 import client
import botocore.exceptions

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from django.db.transaction import atomic

from listTasks.serializers import TasksSerializer
from .permissions import NotForUsers
from profile.utility import get_user_id_by_access
from .services.user_data import update_solution_streak_info, get_user
from .services.tasks import get_task, get_task_by_hash, get_all_tasks

log = logging.getLogger("coding.views")


class ReturnTask(generics.RetrieveAPIView):
    """
    View for return one task to solving
    """

    serializer_class = TasksSerializer

    def get_queryset(self):
        return get_all_tasks()

    def get_object(self):
        return get_task_by_hash(self.kwargs["name"])


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
def get_user_by_token(request, access_token):
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

    @atomic()
    def post(self, request):

        task_id = request.data.get("task_id", None)
        user_id = request.data.get("id", None)

        if not (all((task_id, user_id))):
            log.error("Not enough information to save")
            return Response("Not enough information to save", status=status.HTTP_400_BAD_REQUEST)

        user = get_user(user_id)
        task = get_task(task_id)
        if user is None or task is None:
            log.error(f"User or task is not found: task - {task_id}, user - {user_id}")
            return Response(f"User or task is not found: task - {task_id}, user - {user_id}",
                            status=status.HTTP_404_NOT_FOUND)

        update_solution_streak_info(user_id=user_id, user=user, task=task)

        return Response("Success data save", status=status.HTTP_200_OK)
