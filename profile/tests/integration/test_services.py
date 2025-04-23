import pytest

from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.utils.serializer_helpers import ReturnDict

from profile.services import get_refresh_token, logout_user, return_user_data_for_profile

factory = APIRequestFactory()


@pytest.mark.django_db
@pytest.mark.parametrize(
    "username",
    (
            ("testuser-1"),
            ("testuser-2"),
    )
)
def test_get_refresh_token(username):
    user = User.objects.get(username=username)

    result = get_refresh_token(user)

    assert 'refresh' in result
    assert 'access' in result

    refresh_token = RefreshToken(result['refresh'])
    access_token = refresh_token.access_token

    assert refresh_token.payload['user_id'] == user.id
    assert refresh_token.payload['username'] == user.username
    assert 'exp' in refresh_token.payload
    assert 'jti' in refresh_token.payload

    assert access_token.payload['user_id'] == user.id
    assert 'exp' in access_token.payload
    assert 'jti' in access_token.payload


@pytest.mark.parametrize(
    "refresh",
    (
        "fake_string",
        None
    )
)
@pytest.mark.django_db
def test_logout_user(refresh):
    if refresh is not None:
        refresh_token_str = refresh
        assert logout_user(refresh_token_str) is None
    else:
        user = User.objects.get(username="testuser-1")
        refresh_token = RefreshToken.for_user(user)
        refresh_token_str = str(refresh_token)

        logout_user(refresh_token_str)

        with pytest.raises(TokenError) as excinfo:
            RefreshToken(refresh_token_str)

        assert "Token is blacklisted" in str(excinfo.value)

@pytest.mark.parametrize(
    "user_id, exp_result",
    (
        (2, ReturnDict),
        (999, None)
    )
)
@pytest.mark.django_db
def test_return_user_data_for_profile(user_id, exp_result):
    result = return_user_data_for_profile(user_id)
    if exp_result is not None:
        assert type(result) == exp_result
    else:
        assert result is None