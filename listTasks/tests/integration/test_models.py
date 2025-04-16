import pytest
from hashlib import sha224

from listTasks.models import Task, Type, ExamplesForTask


class TestTask:
    @pytest.mark.django_db(transaction=True)
    def test_task_create(self):
        type_for_task = Type.objects.create(catTask="Alg")
        example_task = ExamplesForTask.objects.create(python="sdaf", cpp="asdf", go="asdf")
        task = Task.objects.create(name="testName", desc="desc", cat=type_for_task, patterns=example_task, first_test="asdf",
                            second_test="asdf", third_test="asdf", cost=100, level="E")

        assert task.name == "testName"
        assert task.hash_name ==  sha224("testName".encode()).hexdigest()[:9]
        assert task.cost == 100
        assert str(task) == "testName"

    @pytest.mark.django_db
    def test_task_menu_manager(self):
        assert Task.tasks_menu.count() == Task.objects.filter().count()
