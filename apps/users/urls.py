from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from django.urls import path
from .views import UserRegisterView , JwtTokenObtainView

urlpatterns = [
    path('signup',UserRegisterView.as_view(),name="user-signup"),
    path('login',JwtTokenObtainView.as_view(),name="user-login"),
    # path('token/refresh', TokenRefreshView.as_view(), name="token-refresh"),
]