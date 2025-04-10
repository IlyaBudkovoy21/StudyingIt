import logging

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

from .serializers import ProfileSerializer, TokenSerializer
from .models import CustomUser, DatesInfoUser
from .utility import get_user_id_by_access
from .services import registration_user, logout_user, return_user_data_for_profile

logger = logging.getLogger('profile.views')


class Registration(APIView):
    def post(self, request):
        token = registration_user(request.data)
        if token:
            return Response(token, status=status.HTTP_201_CREATED)
        return Response("Uncorrect data to registration user", status=status.HTTP_302_FOUND)


class Logout(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh_token")
        if not refresh_token:
            return Response("Необходим refresh токен", status=status.HTTP_400_BAD_REQUEST)

        result_logout = logout_user(refresh_token)
        if result_logout:
            return Response("Успешный выход", status=status.HTTP_200_OK)
        return Response("Неверный refresh токен", status=status.HTTP_400_BAD_REQUEST)



class Profile(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        token = request.META.get('HTTP_AUTHORIZATION', '')
        bear, token = token.split()
        if token:
            user = get_user_id_by_access(token)
            if user["status"] == "OK":
                user_id = user["data"]
                info = return_user_data_for_profile(user_id)
                if info:
                    return Response(info, status=status.HTTP_200_OK)
                logger.warning("Failure when trying to get data from the database")
                return Response("Failure when trying to get data from the database",
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response(data="Incorrect token processing", status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(data="Invalid token", status=status.HTTP_401_UNAUTHORIZED)
