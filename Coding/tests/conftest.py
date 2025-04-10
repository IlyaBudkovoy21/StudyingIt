from django.contrib.auth.models import User

import pytest
from datetime import datetime, timedelta

from profile.models import DatesInfoUser
from listTasks.models import Task, Type, ExamplesForTask


@pytest.fixture(autouse=True, scope="session")
@pytest.mark.django_db
def create_db_data(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        types_data = [
            {"catTask": "Arrays"},
            {"catTask": "Strings"},
            {"catTask": "Recursion"},
            {"catTask": "Dynamic Programming"},
        ]
        types_instances = []
        for data in types_data:
            types_instances.append(Type.objects.create(**data))

        code_patterns_data = [
            {"python": "# Python pattern 1", "cpp": "// C++ pattern 1", "go": "// Go pattern 1"},
            {"python": "# Python pattern 2", "cpp": "// C++ pattern 2", "go": "// Go pattern 2"},
            {"python": "# Python pattern 3", "cpp": "// C++ pattern 3", "go": "// Go pattern 3"},
            {"python": "# Python pattern 4", "cpp": "// C++ pattern 4", "go": "// Go pattern 4"},
        ]
        code_patterns_instances = []
        for data in code_patterns_data:
            code_patterns_instances.append(ExamplesForTask.objects.create(**data))

        tasks_data = [
            {
                "name": "Reverse Array",
                "desc": "Reverse the elements of an array.",
                "cat": types_instances[0],
                "patterns": code_patterns_instances[0],
                "first_test": "input = [1, 2, 3]",
                "second_test": "output = [3, 2, 1]",
                "third_test": "other_input = [4,5,6]",
                "cost": 5,
                "level": "E",
            },
            {
                "name": "Check Palindrome",
                "desc": "Determine if a string is a palindrome.",
                "cat": types_instances[1],
                "patterns": code_patterns_instances[1],
                "first_test": "input = 'madam'",
                "second_test": "output = True",
                "third_test": "other_input = 'level'",
                "cost": 10,
                "level": "M",
            },
            {
                "name": "Fibonacci Sequence",
                "desc": "Generate the Fibonacci sequence using recursion.",
                "cat": types_instances[2],
                "patterns": code_patterns_instances[2],
                "first_test": "n = 5",
                "second_test": "output = [0, 1, 1, 2, 3]",
                "third_test": "other_input = n = 10",
                "cost": 15,
                "level": "H",
            },
            {
                "name": "Coin Change",
                "desc": "Find the minimum number of coins to make change.",
                "cat": types_instances[3],
                "patterns": code_patterns_instances[3],
                "first_test": "coins = [1, 2, 5], amount = 11",
                "second_test": "output = 3",
                "third_test": "coins = [2], amount = 3",
                "cost": 20,
                "level": "H",
            },
        ]
        tasks_instances = []
        for data in tasks_data:
            tasks_instances.append(Task.objects.create(**data))

        date_streaks = [None,
                        (datetime(2023, 12, 31, 15, 30, 0), 13, 4),
                        (datetime.now().date(), 13, 1),
                        (datetime.now().date() - timedelta(days=1), 13, 1),
                        (datetime.now().date() - timedelta(days=2), 13, 1),
                        (datetime.now().date() - timedelta(days=5), 0, 5),
                        (datetime.now().date() - timedelta(days=6), 13, 5),
                        (datetime.now().date() - timedelta(days=6), 1, 6)]

        for user_id in range(1, 9):
            user = User.objects.create(username=f"testuser-{user_id}")
            streak = date_streaks[user_id - 1]
            if not (streak is None):
                day_start_row, max_days, days_in_row = streak
                DatesInfoUser.objects.create(user=user, day_start_row=day_start_row, max_days=max_days,
                                             days_in_row=days_in_row)

