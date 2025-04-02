from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory
from rest_framework import status

import pytest
from datetime import datetime, timedelta

from listTasks.models import Tasks
from Coding.views import CodeMonitoring
from Coding.tests.unit_tests.mocks import MockDatesInfoUser


@pytest.mark.usefixtures("create_db_data")
class TestCodeMonitoring:
    @pytest.mark.parametrize(
        "id, task_id, exp_status",
        [
            [1, 1, status.HTTP_200_OK],
        ]
    )
    @pytest.mark.django_db
    def test_post(self, id, task_id, exp_status):

        data = {}
        if id is not None:
            data["id"] = id
        if task_id is not None:
            data["task_id"] = task_id

        request = APIRequestFactory().post("/api/complete/", data=data)
        CodeMonitoring.permission_classes = []
        response = CodeMonitoring.as_view()(request)

        assert response.status_code == exp_status
