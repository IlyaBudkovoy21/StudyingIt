from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated

from .models import CustomUser, DatesInfoUser
from django.contrib.auth.models import User
from .utility import get_username_by_access


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
            username = get_username_by_access(token)
            if username["status"] == "OK":
                username = username["data"]
                try:
                    user = User.objects.only("id", "username").get(username=username)
                    user_info = DatesInfoUser.objects.defer("day_start_row").get(pk=user.id)
                    return Response({"username": user.username, "max_days": user_info.max_days,
                                     "current_days_row": user_info.days_in_row})
                except Exception as e:
                    print(e)
                    return Response({"detail": "Incorrect token processing"}, status=500)
            else:
                return Response(data={"detail": "Unvalid token"}, status=401)
        else:
            return Response(data={"detail": "Unvalid token"}, status=401)