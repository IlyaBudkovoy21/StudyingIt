
from django.urls import path
from . import views


urlpatterns = [
    path('', views.ListTasks.as_view(), name='tasks'),
]
