import pytest
from typing import Optional
from hashlib import sha224
from datetime import datetime, timedelta

from django.contrib.auth.models import User

from profile.models import DatesInfoUser
from listTasks.models import Task
from coding.services.user_data import get_user, update_user_streak, update_solution_streak_info
from coding.services.tasks import get_all_tasks, get_task_by_hash, get_task


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_id, exp_result",
    (
            (1, User),
            (999, None),
            ("asdfasdf", None)
    )
)
def test_get_user(user_id: int, exp_result: Optional[User]):
    result = get_user(user_id)

    if exp_result is None:
        assert result is None
    else:
        exp_result = User.objects.get(id=user_id)
        assert result == exp_result


@pytest.mark.parametrize(
        "user_id, task_id, exp_data, exp_max_days, exp_days_row",
        [
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
def test_post_user_info(user_id, task_id, exp_data, exp_max_days, exp_days_row):
    user = User.objects.get(id=user_id)
    dates = DatesInfoUser.objects.get(user=user)

    update_user_streak(dates)

    assert dates.day_start_row == exp_data
    assert dates.days_in_row == exp_days_row
    assert dates.max_days == exp_max_days


@pytest.mark.parametrize(
    "user_id, task_id",
    (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 1),
        (6, 2),
        (7, 3),
        (8, 4),
    )
)
@pytest.mark.django_db
def test_update_solution(user_id, task_id):

    task = Task.objects.get(id=task_id)
    user = User.objects.get(id=user_id)

    update_solution_streak_info(user_id=user_id, user=user, task=task)

    assert DatesInfoUser.objects.filter(user_id=user_id).exists()
    assert task.users_solved.filter(pk=user_id).exists()



# Tasks


@pytest.mark.django_db
@pytest.mark.parametrize(
    "task_id, exp_result",
    (
            (1, Task),
            (2, Task),
            (999, None),
            ("sdf", None),
    )
)
def test_get_task_by_id(task_id: int, exp_result: Optional[Task]):
    result = get_task(task_id)

    if exp_result is None:
        assert result is None
    else:
        task = Task.objects.get(id=task_id)
        assert task.name == result.name

@pytest.mark.django_db
def test_get_all_tasks():
    result = get_all_tasks()
    assert len(result) == 4


@pytest.mark.parametrize(
    "name",
    (
            "Reverse Array",
            "Check Palindrome",
            "Fibonacci Sequence",
            "Coin Change"
    )
)
@pytest.mark.django_db
def test_get_task_by_hash(name: str):
    hash_name = sha224(name.encode()).hexdigest()[:9]
    task = Task.objects.get(name=name)
    result = get_task_by_hash(hash_name)
    assert result.name == task.name
