from django.contrib.auth.models import User

import pytest

from PersonalAccount.models import DatesInfoUser
from listTasks.models import Tasks
from .mocks import MockTasksGet, mock_db_users, MockDatesInfoUser


@pytest.fixture(autouse=True)
def create_db_mocks(monkeypatch):
    monkeypatch.setattr(User.objects, "get", mock_db_users)
    monkeypatch.setattr(Tasks.objects, "only", MockTasksGet)



