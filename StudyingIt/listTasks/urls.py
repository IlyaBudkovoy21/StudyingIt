
from django.urls import path
from . import views


urlpatterns = [
    path('<str:cat>/all/', views.ListTasks.as_view(), name='tasks')
]
