from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated

import logging

from .models import CustomUser, DatesInfoUser
from django.contrib.auth.models import User
from .utility import get_user_id_by_access

logger = logging.getLogger('PersonalAccount.views')


class Registration(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            refresh.payload.update({
                "user_id": user.id,
                "username": user.username
            }
            )
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_302_FOUND)


class Logout(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh_token")
        if not refresh_token:
            return Response({"error": "Необходим refresh токен"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception as e:
            return Response({
                "error": "Неверный refresh токен"
            }, status=status.HTTP_400_BAD_REQUEST)
        return Response({"success": "Успешный выход"}, status=status.HTTP_200_OK)


class Profile(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        token = request.META.get('HTTP_AUTHORIZATION', '')
        bear, token = token.split()
        if token:
            user = get_user_id_by_access(token)
            if user["status"] == "OK":
                id = user["data"]
                print(id)
                try:
                    user = User.objects.only("id", "username").get(id=id)
                    user_info = DatesInfoUser.objects.defer("day_start_row").get(pk=user.id)
                    solved_tasks = list(user.tasks_set.all().only("id").values_list("id", flat=True))
                    return Response({"username": user.username, "max_days": user_info.max_days,
                                     "current_days_row": user_info.days_in_row, "tasks": solved_tasks})
                except Exception as e:
                    logger.warning(e)
                    return Response({"detail": "Failure when trying to get data from the database"},
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response(data={"detail": "Incorrect token processing"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(data={"detail": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)
