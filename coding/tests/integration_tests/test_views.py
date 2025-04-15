import pytest
from datetime import datetime, timedelta
from contextlib import nullcontext
from django.http import Http404

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.test import APIRequestFactory
from rest_framework import status
from django.contrib.auth.models import User

from coding.views import CodeMonitoring, get_user_by_token, ReturnTask
from profile.models import DatesInfoUser

factory = APIRequestFactory()


class TestCodeMonitoring:
    NONEXISTS_ID = 999

    @pytest.mark.parametrize(
        "id, task_id, exp_status",
        [
            [None, 1, status.HTTP_400_BAD_REQUEST],
            [1, None, status.HTTP_400_BAD_REQUEST],
            [None, None, status.HTTP_400_BAD_REQUEST],
            [NONEXISTS_ID, None, status.HTTP_400_BAD_REQUEST],
            [None, NONEXISTS_ID, status.HTTP_400_BAD_REQUEST],
            [1, None, status.HTTP_400_BAD_REQUEST],
            [NONEXISTS_ID, 2, status.HTTP_404_NOT_FOUND],
            [2, NONEXISTS_ID, status.HTTP_404_NOT_FOUND],
            [NONEXISTS_ID, NONEXISTS_ID, status.HTTP_404_NOT_FOUND],
            [1, 1, status.HTTP_200_OK],
        ]
    )
    @pytest.mark.django_db
    def test_post_status(self, id, task_id, exp_status):

        data = {}
        if id is not None:
            data["id"] = id
        if task_id is not None:
            data["task_id"] = task_id

        request = factory.post("/api/complete/", data=data)
        CodeMonitoring.permission_classes = []
        response = CodeMonitoring.as_view()(request)

        assert response.status_code == exp_status

    @pytest.mark.parametrize(
        "user_id, task_id, exp_data, exp_max_days, exp_days_row",
        [
            [1, 1, datetime.now().date(), 1, 1],
            [2, 2, datetime.now().date(), 13, 1],
            [3, 3, datetime.now().date(), 13, 1],
            [4, 4, datetime.now().date() - timedelta(days=1), 13, 2],
            [5, 1, datetime.now().date(), 13, 1],
            [6, 2, datetime.now().date() - timedelta(days=5), 6, 6],
            [7, 3, datetime.now().date(), 13, 1],
            [8, 4, datetime.now().date() - timedelta(days=6), 7, 7],
        ]
    )
    @pytest.mark.django_db
    def test_post_user_info(self, user_id, task_id, exp_data, exp_max_days, exp_days_row):
        request = factory.post("/api/complete/", data={"id": user_id,
                                                       "task_id": task_id}, format='json')
        CodeMonitoring.permission_classes = []
        CodeMonitoring.as_view()(request)

        user = User.objects.get(id=user_id)
        dates = DatesInfoUser.objects.get(user=user)

        assert dates.day_start_row == exp_data
        assert dates.days_in_row == exp_days_row
        assert dates.max_days == exp_max_days


@pytest.mark.parametrize(
    "username, password, exp_id",
    (
            ("testuser-1", "testuser-1-password", "1"),
            ("testuser-2", "testuser-2-password", "2"),
            ("testuser-3", "testuser-3-password", "3"),
    )
)
@pytest.mark.django_db
def test_get_user_by_token(username, password, exp_id):
    request_for_token = factory.post("/api/token/", data={"username": username,
                                                          "password": password}, format='json')
    response = TokenObtainPairView.as_view()(request_for_token).render()

    refresh = response.data.get("refresh", None)
    access = response.data.get("access", None)

    request_test = factory.get(f"/api/code/auth/", headers={"Authorization": f"Bearer {access}"})
    result = get_user_by_token(request_test)

    assert result.data.get("user_id", None) == exp_id


class TestReturnTask:
    @pytest.mark.parametrize(
        "hash_name, task_id, exp_status",
        (
                ('563bf3a98', 1, status.HTTP_200_OK),
                ('d19d0f9b7', 3, status.HTTP_200_OK),
                ("894d741f9", 4, status.HTTP_200_OK),
                ("failed_test", 1, status.HTTP_404_NOT_FOUND)
        )
    )
    @pytest.mark.django_db
    def test_return_task(self, hash_name, task_id, exp_status):
        request = factory.get(f"/api/code/{hash_name}/")
        response = ReturnTask.as_view()(request, hash_name=hash_name)
        assert response.status_code == exp_status
        if exp_status == status.HTTP_200_OK:
            assert response.data.get("id", None) == task_id
