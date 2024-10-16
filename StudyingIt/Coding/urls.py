from django.urls import path
from . import views


urlpatterns = [
    path("checkTask/", views.SaveCode.as_view()),
    path('<slug:name>/', views.ReturnTask.as_view())
]
