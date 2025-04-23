import pytest
from typing import Optional

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.test import APIRequestFactory

from profile.utility import get_user_id_by_access


@pytest.mark.django_db
@pytest.mark.parametrize(
    "username, password, exp_result",
    (
            ("testuser-1", "testuser-1-password", '1'),
            ("testuser-2", "testuser-2-password", '2'),
            (None, None, None)

    )
)
def test_get_user_id_by_access(username: str, password: str, exp_result: Optional[str]):
    if username is None and password is None:
        access_token = "random_string"
    else:
        request = APIRequestFactory().post("api/token/", data={"username": username, "password": password},
                                           format="json")
        response = TokenObtainPairView().as_view()(request)
        access_token = response.data.get("access", None)

    if exp_result is None:
        assert get_user_id_by_access(access_token) is exp_result
    else:
        assert get_user_id_by_access(access_token) == exp_result
