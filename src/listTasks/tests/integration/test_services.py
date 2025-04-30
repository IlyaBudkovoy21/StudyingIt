import pytest
import json

from django.db.models import Q

from listTasks.models import Task
from listTasks.services import return_task_by_one_cat, return_tasks_menu, return_many_cats, return_all_types, \
    return_all_tasks



class TestTasks:
    @pytest.mark.parametrize(
        "category_id, exp_result",
        (
            (1, True),
            (2, True),
            (3, True),
            (4, True),
            (999, False),
            (5, False)
        )
    )
    @pytest.mark.django_db
    def test_return_task_by_one_cat(self, category_id: int, exp_result: bool):
        result = return_task_by_one_cat(cat=category_id)
        assert result.exists() == exp_result

    @pytest.mark.django_db
    def test_return_tasks_menu(self):
        result = return_tasks_menu()
        assert result.exists() == True and result.count() == 4

    @pytest.mark.parametrize(
        "categories,expected_count",
        [
            ("[1,2,3]", 3),
            ("[2,3,4]", 3),
            ("[1,0,3]", 2),
            ("[999,1,4]", 2),
            ("[]", 4)
        ]
    )
    @pytest.mark.django_db
    def test_return_many_cats(self, categories:str, expected_count):
        result = return_many_cats(categories)
        categories = json.loads(categories)

        if not categories:
            assert result.count() == expected_count
            return

        assert result.count() == expected_count

        for task in result:
            assert task.cat_id in categories


    @pytest.mark.django_db
    def test_return_all_types(self):
        assert return_all_types().count() == 4

    @pytest.mark.django_db
    def test_return_all_tasks(self):
        assert return_all_tasks().count() == 4