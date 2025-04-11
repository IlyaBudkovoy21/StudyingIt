from django.urls import path, register_converter
from . import views
from . import converters

register_converter(converters.Valid_token, 'token')

urlpatterns = [
    path("auth/<token:access_token>/", views.get_user_by_token),
    path("<slug:hash_name>/", views.ReturnTask.as_view())
]
