import pytest
from contextlib import nullcontext as does_not_raise

from django.contrib.auth.models import User
from rest_framework.serializers import ValidationError

from profile.serializers import UserSerializer, ProfileSerializer, TokenSerializer
from profile.models import DatesInfoUser


class TestUserSerializer:
    @pytest.mark.parametrize(
        "username, password, email, exp_result",
        (
                ("testName", "testPassword", "normal_email@yandex.ru", True),
                ("testName", "testPassword", "ne_normal_emailyandex.ru", False),
                (None, "password", "normal_email@yandex.ru", False),
                ("testName", None, "normal_email@yandex.ru", False),
                ("testName", "password", None, False),
                ("testName", None, None, False),
                (None, "password", None, False),
                (None, None, "normal_email@yandex.ru", False),
                (None, None, None, False),
        )
    )
    def test_user_serializer(self, username, password, email, exp_result):

        data = {}
        if username is not None:
            data["username"] = username
        if password is not None:
            data["password"] = password
        if email is not None:
            data["email"] = email
        serializer = UserSerializer(data=data)
        assert serializer.is_valid() == exp_result

    @pytest.mark.parametrize(
        "validated_data, error",
        (
                ({"username": "testuser-1", "email": "testemail@yandex.ru", "password": "testuser-1-password"},
                 does_not_raise()),
                ({"username": "testuser-1", "password": "testuser-1-password"},
                 pytest.raises(ValidationError)),
                ({"email": "testemail@yandex.ru", "password": "testuser-1-password"},
                 pytest.raises(ValidationError)),
                ({"username": "testuser-1", "email": "testemail@yandex.ru"},
                 pytest.raises(ValidationError))
        )
    )
    @pytest.mark.django_db
    def test_create_user(self, monkeypatch, validated_data, error):
        monkeypatch.setattr(User, "save", lambda instance: None)
        monkeypatch.setattr(DatesInfoUser.objects, "create", lambda user: None)
        with error:
            user = UserSerializer().create(validated_data)
            assert user.username == validated_data["username"]
            assert user.email == validated_data["email"]


@pytest.mark.parametrize(
    "username, max_days, current_days_row, tasks, exp_result",
    (
            ("testuser-1", 10, 20, [{"id": 1, "title": "Task 1", "completed": True},
                                    {"id": 2, "title": "Task 2", "completed": False}], True),
            (None, 10, 20, [{"id": 1, "title": "Task 1", "completed": True},
                                    {"id": 2, "title": "Task 2", "completed": False}], False),
            ("testuser-1", "asdf", 20, [{"id": 1, "title": "Task 1", "completed": True},
                                    {"id": 2, "title": "Task 2", "completed": False}], False),
            ("testuser-1", 10, "asdf", [{"id": 1, "title": "Task 1", "completed": True},
                                    {"id": 2, "title": "Task 2", "completed": False}], False),
            ("testuser-1", 10, 20, {"id": 1, "title": "Task 1", "completed": True}, False),
            ("testuser-1", None, 20, {"id": 1, "title": "Task 1", "completed": True}, False),
            ("testuser-1", 10, None, {"id": 1, "title": "Task 1", "completed": True}, False),
            ("testuser-1", 10, 20, None, False),
    )
)
def test_user_serializer(username, max_days, current_days_row, tasks, exp_result):
    data = {}
    if username is not None:
        data["username"] = username
    if max_days is not None:
        data["max_days"] = max_days
    if current_days_row is not None:
        data["current_days_row"] = current_days_row
    if tasks is not None:
        data["tasks"] = tasks
    serializer = ProfileSerializer(data=data)
    assert serializer.is_valid() == exp_result


@pytest.mark.parametrize(
    "refresh, access, exp_result",
    (
            ("sadf", "asdf", True),
            (None, "asdf", False),
            ("asdf", None, False),
            (None, None, False),
    )
)
def test_user_serializer(refresh, access, exp_result):
    data = {}
    if refresh is not None:
        data["refresh"] = refresh
    if access is not None:
        data["access"] = access
    serializer = TokenSerializer(data=data)
    assert serializer.is_valid() == exp_result
