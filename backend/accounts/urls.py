from django.urls import path
from .views import LoginView, RegisterView, LogoutView
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('register', RegisterView.as_view(), name="register"),
    path('login', LoginView.as_view(), name="login"),
    path('logout', LogoutView.as_view(), name="logout"),
    path('token/refresh', jwt_views.TokenRefreshView.as_view(), name="token_refresh"),
]
