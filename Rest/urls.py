from django.urls import path
from . import views

urlpatterns = [
    path('medications/fetch', views.load_medications, name='fetch_data'),
    path('data/insert', views.populate, name='insert_data'),
    path('token/refresh', views.refresh_access_token, name='token_refresh'),
    path('register', views.register, name='register'),  # Register endpoint
    path('login', views.login, name="login")
]