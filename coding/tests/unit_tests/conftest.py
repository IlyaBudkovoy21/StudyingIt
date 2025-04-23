from django.contrib.auth.models import User

import pytest

from listTasks.models import Task
from coding.tests.unit_tests.mocks import MockTasksGet, mock_db_users


@pytest.fixture(autouse=True)
def create_db_mocks(monkeypatch):
    monkeypatch.setattr(User.objects, "get", mock_db_users)
    monkeypatch.setattr(Task.objects, "only", MockTasksGet)



