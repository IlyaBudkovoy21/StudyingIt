from django.contrib.auth.models import User

import pytest
from datetime import datetime, timedelta

from listTasks.models import Tasks
from Coding.views import CodeMonitoring
from PersonalAccount.models import DatesInfoUser
from .mocks import MockDatesInfoUser


class TestCodeMonitoring:
    @pytest.mark.parametrize(
        "user_id, exp_result",
        [
            (1, User),
            (10, None),
            (7, User),
            (50, None),
        ]
    )
    def test_get_user(self, user_id, exp_result):

        result = CodeMonitoring.get_user(user_id)

        if exp_result is None:
            assert result is None
        else:
            assert isinstance(result, User)
            assert result.username == "testUsername"

    @pytest.mark.parametrize(
        "task_id, exp_result",
        [
            (1, Tasks),
            (10, None),
            (7, Tasks),
            (50, None),
        ]
    )
    def test_get_task(self, task_id, exp_result):

        result = CodeMonitoring.get_task(task_id)

        if exp_result is None:
            assert result is None
        else:
            assert isinstance(result, Tasks)
            assert result.name == "testTaskName"

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

        CodeMonitoring.update_user_streak(test_info)

        assert test_info.day_start_row == exp_data
        assert test_info.max_days == exp_max_days
        assert test_info.days_in_row == exp_days_row
        assert test_info.user.username == username
        assert test_info.user.id == user_id
