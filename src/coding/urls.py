from django.urls import path

from . import views


urlpatterns = [
    path("auth/", views.get_user_by_token),
    path("<slug:hash_name>/", views.ReturnTask.as_view())
]
