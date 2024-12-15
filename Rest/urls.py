from django.urls import path
from . import views

urlpatterns = [
    path('token/refresh', views.RefreshAccessTokenView.as_view(), name='token_refresh'),
    path('register', views.RegisterView.as_view(), name='register'),  # Register endpoint
    path('login', views.LoginView.as_view(), name="login"),
    path('edit', views.EditView.as_view(), name="edit"),
    path('check-url', views.check_url, name='check_url'),
]