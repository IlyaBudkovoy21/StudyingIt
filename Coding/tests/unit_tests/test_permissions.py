import pytest

from rest_framework.test import APIRequestFactory

from StudyingIt.settings import SERVICES
from coding.permissions import NotForUsers

factory = APIRequestFactory()


@pytest.mark.parametrize(
    "HTTP_X_REAL_IP, exp_result",
    (
            (SERVICES[0], True),
            ("127.0.0.1", False),
            ("121.21.21.21", False)
    )
)
def test_not_for_users_permission(HTTP_X_REAL_IP, exp_result):
    request = factory.get("api/code/", HTTP_X_REAL_IP=HTTP_X_REAL_IP)

    assert NotForUsers().has_permission(request, None) == exp_result
