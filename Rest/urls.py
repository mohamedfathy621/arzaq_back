from django.urls import path
from . import views

urlpatterns = [
    path('medications/order', views.IssueOrderView.as_view(), name='fetch_data'),
    path('medications/fetch', views.LoadMedicationsView.as_view(), name='fetch_data'),
    path('data/insert', views.populate, name='insert_data'),
    path('token/refresh', views.RefreshAccessTokenView.as_view(), name='token_refresh'),
    path('register', views.RegisterView.as_view(), name='register'),  # Register endpoint
    path('login', views.LoginView.as_view(), name="login")
]