import pytest
from datetime import datetime, timedelta

from django.contrib.auth.models import User

from listTasks.models import Task
from coding.tests.unit_tests.mocks import MockDatesInfoUser
from coding.services.user_data import update_user_streak, get_user
from coding.services.tasks import get_task


class TestUserData:
    @pytest.mark.parametrize(
        "username, user_id, day_start_row, max_days, days_in_row, exp_data, exp_max_days, exp_days_row",
        (
                ["testUsername1", 1, None, 0, 0, datetime.now().date(), 1, 1],
                ["testUsername2", 2, datetime(2023, 12, 31, 15, 30, 0), 13, 4,
                 datetime.now().date(), 13, 1],
                ["testUsername3", 3, datetime.now().date(), 13, 1, datetime.now().date(), 13, 1],
                ["testUsername4", 4, datetime.now().date() - timedelta(days=1), 13, 1,
                 datetime.now().date() - timedelta(days=1), 13, 2],
                ["testUsername5", 5, datetime.now().date() - timedelta(days=2), 13, 1,
                 datetime.now().date(), 13, 1],
                ["testUsername6", 6, datetime.now().date() - timedelta(days=5), 0, 5,
                 datetime.now().date() - timedelta(days=5), 6, 6],
                ["testUsername7", 7, datetime.now().date() - timedelta(days=6), 13, 5,
                 datetime.now().date(), 13, 1],
                ["testUsername8", 8, datetime.now().date() - timedelta(days=6), 1, 6,
                 datetime.now().date() - timedelta(days=6), 7, 7],
        )
    )
    def test_update_user_streak(self, username, user_id, day_start_row, max_days, days_in_row, exp_data, exp_max_days,
                                exp_days_row):
        test_user = User(id=user_id, username=username)
        test_info = MockDatesInfoUser(user=test_user)
        test_info.day_start_row = day_start_row
        test_info.max_days = max_days
        test_info.days_in_row = days_in_row

        update_user_streak(test_info)

        assert test_info.day_start_row == exp_data
        assert test_info.max_days == exp_max_days
        assert test_info.days_in_row == exp_days_row
        assert test_info.user.username == username
        assert test_info.user.id == user_id


    @pytest.mark.parametrize(
            "user_id, exp_result",
            [
                (1, User),
                (10, None),
                (7, User),
                (50, None),
                ("asdfasdfasdf", None),
            ]
        )
    def test_get_user(self, user_id, exp_result):

        result = get_user(user_id)

        if exp_result is None:
            assert result is None
        else:
            assert isinstance(result, User)
            assert result.username == "testUsername"




class TestTasksServices:
    @pytest.mark.parametrize(
        "task_id, exp_result",
        [
            (1, Task),
            (10, None),
            (7, Task),
            (50, None),
            ("asdfasdf", None)
        ]
    )
    def test_get_task(self, task_id, exp_result):

        result = get_task(task_id)

        if exp_result is None:
            assert result is None
        else:
            assert isinstance(result, Task)
            assert result.name == "testTaskName"

