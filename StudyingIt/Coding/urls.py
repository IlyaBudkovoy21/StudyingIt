from django.urls import path
from . import views


urlpatterns = [
    path("checkTask/", views.SaveCode.as_view()),
    path('<str:namex>/', views.ReturnTask.as_view())
]
