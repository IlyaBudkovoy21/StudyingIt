from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from . import views

urlpatterns = [
    path('registration/', views.Registration.as_view()),
    path('login/', TokenObtainPairView.as_view()),
    path("logout/", views.Logout.as_view())
]
