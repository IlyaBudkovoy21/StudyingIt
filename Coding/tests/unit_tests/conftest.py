from django.contrib.auth.models import User

import pytest

from listTasks.models import Tasks
from Coding.tests.unit_tests.mocks import MockTasksGet, mock_db_users


@pytest.fixture(autouse=True)
def create_db_mocks(monkeypatch):
    monkeypatch.setattr(User.objects, "get", mock_db_users)
    monkeypatch.setattr(Tasks.objects, "only", MockTasksGet)



