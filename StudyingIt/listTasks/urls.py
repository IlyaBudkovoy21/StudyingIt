from django.urls import path
from . import views

urlpatterns = [
    path('<int:cat>/all/', views.ListTasksByCat.as_view(), name='tasks_one_cat'),
    path('all/', views.AllTasks.as_view(), name='listTasks'),
    path('<int:seq_num>/', views.OneTask.as_view(), name='oneTask'),
    path('addTask/', views.AddTask.as_view(), name='addTask')
]
