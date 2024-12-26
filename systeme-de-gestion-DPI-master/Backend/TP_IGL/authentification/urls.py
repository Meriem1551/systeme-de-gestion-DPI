from unicodedata import name
from django.urls import path
from .views import LoginUserView, AddUserView, RegisterView

from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [

    path('login/', LoginUserView.as_view(), name='login-user'),

    path('add-user/', RegisterView.as_view(), name='add_user'),

    ]
