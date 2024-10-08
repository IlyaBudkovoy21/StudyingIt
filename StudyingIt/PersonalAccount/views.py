from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer


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


class Login(APIView):
    def post(self, request):
        data = request.data
        username = data.get("username", None)
        password = data.get("password", None)
        if username is None or password is None:
            return Response(
                {"error": "Нужен логин и пароль"},
                status=status.HTTP_400_BAD_REQUEST
            )
        user = authenticate(username=username, password=password)
        if user is None:
            return Response(
                {"error": "Такой пользователь не существует"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        refresh_token = RefreshToken.for_user(user)
        refresh_token.payload.update({
            "user_id": user.id,
            "username": user.username
        }
        )
        return Response({
            "refresh": str(refresh_token),
            "access": str(refresh_token.access_token)
        }, status=status.HTTP_200_OK)


class Logout(APIView):
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
