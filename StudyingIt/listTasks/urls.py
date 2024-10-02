from django.urls import path, include
from . import views
from rest_framework import routers


router = routers.SimpleRouter()
router.register(r'', views.TasksCreateListViewsSet)

urlpatterns = [
    path('<int:cat>/all/', views.ListTasksByCat.as_view(), name='tasks_one_cat'),
    path('tasks/', include(router.urls))
]
