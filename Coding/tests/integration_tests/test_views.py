from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory
from rest_framework import status

import pytest
from datetime import datetime, timedelta

from profile.models import DatesInfoUser
from coding.views import CodeMonitoring


@pytest.mark.usefixtures("create_db_data")
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

        request = APIRequestFactory().post("/api/complete/", data=data)
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
        request = APIRequestFactory().post("/api/complete/", data={"id":user_id,
                                                                   "task_id": task_id}, format='json')
        CodeMonitoring.permission_classes = []
        CodeMonitoring.as_view()(request)

        user = User.objects.get(id=user_id)
        dates = DatesInfoUser.objects.get(user=user)

        assert dates.day_start_row == exp_data
        assert dates.days_in_row == exp_days_row
        assert dates.max_days == exp_max_days
