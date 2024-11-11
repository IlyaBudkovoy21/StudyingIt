import pytest
from listTasks.views import ListTasksByCat
from listTasks.models import Tasks
from hashlib import sha224


@pytest.mark.django_db
class TestListTasksViews:
    def test_list_by_cat(self):
        a = Tasks.objects.get(id=1)
        assert a.hash_name == sha224(a.name.encode()).hexdigest()[:9]
