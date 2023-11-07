from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_api_view),
    path('signup/', views.signup_api_view),
    path('users/confirm/<int:userid>/', views.confirm_user_api_view),
]