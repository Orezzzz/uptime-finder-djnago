from . import views
from django.urls import path


urlpatterns = [
    path('register/', views.RegisterAPI.as_view(), name="signup"),
    path('login/', views.LoginAPI.as_view(), name="login"),
]
