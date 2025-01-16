from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from debug_toolbar.toolbar import debug_toolbar_urls

urlpatterns = [
    path('api/admin/', admin.site.urls),
    path('api/tasksAPI/', include('listTasks.urls')),
    path('api/code/', include("Coding.urls")),
    path('api/account/', include("PersonalAccount.urls")),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
] + debug_toolbar_urls()
