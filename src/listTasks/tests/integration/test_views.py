import pytest

from rest_framework.test import APIRequestFactory
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.status import HTTP_403_FORBIDDEN, HTTP_200_OK

from listTasks.models import ExamplesForTask
from listTasks.views import ListTasksByCat, TasksRetrieveListViewsSet, ReturnAllCategories

factory = APIRequestFactory()


@pytest.mark.django_db
@pytest.mark.parametrize(
    "category, count",
    (
            (1, 1),
            (2, 1),
            (4, 1),
            (99, 0)
    )
)
def test_list_tasks_by_cat(category: int, count: int):
    request = factory.get(f"{category}/all/")
    response = ListTasksByCat.as_view()(request, cat=category)
    assert response.data["count"] == count


@pytest.mark.django_db
def test_tasks_retrieve_list():
    request = factory.get(f"/tasksAPI/tasks/")
    response = TasksRetrieveListViewsSet.as_view({"get": "list"})(request)

    assert response.data.get("count", None) == 4


@pytest.mark.django_db
def test_create_destroy_view_set():
    request = factory.get(f"/tasksAPI/tasks_admin/")
    response = TasksRetrieveListViewsSet.as_view({"get": "list"})(request)

    assert response.data.get("count", None) == 4


@pytest.mark.django_db
def test_all_types_view():
    request = factory.get(f"/tasksAPI/all_cat/")
    response = ReturnAllCategories.as_view()(request)

    assert response.data.get("count", None) == 4
