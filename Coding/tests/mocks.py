from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User

from listTasks.models import Tasks
from PersonalAccount.models import DatesInfoUser


class MockTasksGet:
    def __init__(self, *args):
        pass

    def get(self, id):
        if id in (1, 2, 3, 4, 5, 6, 7, 8, 9):
            return Tasks(name="testTaskName")
        raise ObjectDoesNotExist


def mock_db_users(id):
    if id in (1, 2, 3, 4, 5, 6, 7, 8, 9):
        return User(username="testUsername")
    raise ObjectDoesNotExist


class MockDatesInfoUser(DatesInfoUser):
    def save(self):
        return None
