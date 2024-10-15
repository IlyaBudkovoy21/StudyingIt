from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'', views.TasksRetrieveListViewsSet)

router1 = routers.SimpleRouter()
router1.register(r'', views.CreateDestroyViewSet)



urlpatterns = [
    path('<int:cat>/all/', views.ListTasksByCat.as_view(), name='tasks_one_cat'),
    path('tasks/', include(router.urls)),
    path('tasks_admin/', include(router1.urls)),
    path('filter_tasks/',views.FilterTasksByManyCats.as_view()),
]
