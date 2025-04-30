import pytest

from django.contrib.auth.models import User
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.test import APIRequestFactory
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_302_FOUND, HTTP_200_OK, \
    HTTP_401_UNAUTHORIZED

from profile.views import Registration, Logout, Profile

factory = APIRequestFactory()


@pytest.mark.django_db()
@pytest.mark.parametrize(
    "username, password, email, exp_result",
    (
            ("testuser-3", "testuser-10-password", "email2@gmail.com", HTTP_400_BAD_REQUEST),
            ("testuser-9", "testuser-9-password", "email@gmail.com", HTTP_201_CREATED),
            ("testuser-10", "testuser-10-password", "email2@gmail.com", HTTP_201_CREATED),
            ("testuser-11", "testuser-11-password", "bad_mail.gmail.com", HTTP_302_FOUND),

    )
)
def test_registration_view(username, password, email, exp_result):
    request = factory.post("api/account/registration/", data={"username": username, "password": password,
                                                              "email": email}, format="json")
    response = Registration.as_view()(request)


    assert response.status_code == exp_result
    if exp_result == HTTP_201_CREATED:
        User.objects.filter(username=username).delete()


@pytest.mark.django_db()
@pytest.mark.parametrize(
    "username, password, exp_result",
    (
            ("testuser-1", "testuser-1-password", HTTP_200_OK),
    )
)
def test_logout_view(username, password, exp_result):
    request_for_token = factory.post("/api/token/", data={"username": username, "password": password},
                                     format="json")
    response_for_token = TokenObtainPairView.as_view()(request_for_token)
    refresh_token = response_for_token.data.get("refresh", None)
    access_token = response_for_token.data.get("access", None)

    request = factory.post("/api/account/logout/", data={"refresh_token": refresh_token},
                           headers={"Authorization": f"Bearer {access_token}"})
    response = Logout.as_view()(request)
    assert response.status_code == exp_result

    request = factory.post("/api/account/logout/",
                           headers={"Authorization": f"Bearer {access_token}"})
    response = Logout.as_view()(request)
    assert response.status_code == HTTP_400_BAD_REQUEST

    request = factory.post("/api/account/logout/", data={"refresh_token": "uncorrect_refresh"},
                           headers={"Authorization": f"Bearer {access_token}"})
    response = Logout.as_view()(request)
    assert response.status_code == HTTP_400_BAD_REQUEST


@pytest.mark.parametrize(
    "token, exp_result",
    (
            ("correct", HTTP_200_OK),
            ("", HTTP_401_UNAUTHORIZED),
            ("uncorrect_token", HTTP_401_UNAUTHORIZED),
    )
)
@pytest.mark.django_db
def test_profile(token, exp_result):
    if token == "correct":
        request_for_token = factory.post("/api/token/",
                                         data={"username": "testuser-2", "password": "testuser-2-password"},
                                         format="json")
        response_for_token = TokenObtainPairView.as_view()(request_for_token)
        token = response_for_token.data.get("access", None)
    request = factory.get("/api/account/logout/",
                          headers={"Authorization": f"Bearer {token}"})
    response = Profile.as_view()(request)

    assert response.status_code == exp_result
