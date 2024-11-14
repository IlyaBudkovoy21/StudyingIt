import pytest
from listTasks.views import ListTasksByCat
from listTasks.models import Tasks, Types, CodePatterns
from hashlib import sha224


class TestListTasksViews:
    @pytest.mark.django_db(databases=["default", "test"])
    def test_list_by_cat(self, django_db_use_migrations, django_db_createdb):
        t = Types.objects.using("test").create(catTask="Programming")
        pat = CodePatterns.objects.using("test").create(python="sdaf", cpp="asdf", go="kadsf")
        check = Tasks.objects.using("test").create(
            name="Sum of two numbers",
            desc="Desc sum of two numbers",
            cat=t,
            patterns=pat,
            first_test="asdf",
            second_test="asdf",
            cost=100
        )
        assert check.hash_name == sha224(check.name.encode()).hexdigest()[:9]
