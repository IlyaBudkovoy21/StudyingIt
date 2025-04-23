import pytest

from django.contrib.auth.models import User

from profile.services import registration_user
from profile.serializers import UserSerializer


@pytest.mark.parametrize(
    "username, email, password, exp_result",
    (
        ("Ilya21", "Ilya21@gmail.com", "Ilya21password", User),
        ("RayanGosling","drive@gmail.com", None, None),
        ("DwayneJohnson", None, "DwayneJohnsonPassword", None),
        (None, "ivan_zolo@gmail.com", "IvanZolo2004password", None),
        (None,"drive@gmail.com", None, None),
        ("DwayneJohnson", None, None, None),
        (None, None, "IvanZolo2004password", None),
        ("RayanGosling", "drive@gmail.com", "", None),
        ("DwayneJohnson", "", "DwayneJohnsonPassword", None),
        ("", "ivan_zolo@gmail.com", "IvanZolo2004password", None),
        ("RayanGosling", "", "", None),
        ("", "", "DwayneJohnsonPassword", None),
        ("", "ivan_zolo@gmail.com", "", None),
        (None, None, None, None),
        (None, None, None, None),

    )
)
def test_registration_user(monkeypatch, username, email, password, exp_result):
    monkeypatch.setattr(UserSerializer, "save", lambda self: User)

    data = {}
    if username is not None:
        data["username"] = username
    if email is not None:
        data["email"] = email
    if password is not None:
        data["password"] = password

    result = registration_user(data)

    assert result is exp_result


