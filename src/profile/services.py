from typing import Optional

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.contrib.auth.models import User

from .serializers import UserSerializer, TokenSerializer
from profile.models import DatesInfoUser
from .serializers import ProfileSerializer


def get_refresh_token(user: User):
    refresh = RefreshToken.for_user(user)
    refresh.payload.update({
        "user_id": user.id,
        "username": user.username
    }
    )
    serialize = TokenSerializer({
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    })
    return serialize.data


def registration_user(data: dict) -> Optional[User]:
    serializer = UserSerializer(data=data)
    if serializer.is_valid():
        user = serializer.save()
        return user
    return None


def logout_user(refresh_token: str) -> Optional[bool]:
    try:
        token = RefreshToken(refresh_token)
        token.blacklist()
    except Exception as e:
        return None
    else:
        return True


def return_user_data_for_profile(user_id: str) -> Optional[dict]:
    try:
        user = User.objects.only("id", "username").get(id=user_id)
        user_info = DatesInfoUser.objects.defer("day_start_row").get(user_id=user.id)
        solved_tasks = list(user.task_set.all().only("id", "level").values("id", "level"))
        serializer = ProfileSerializer({"username": user.username, "max_days": user_info.max_days,
                                        "current_days_row": user_info.days_in_row, "tasks": solved_tasks})
        return serializer.data
    except Exception as e:
        return None
