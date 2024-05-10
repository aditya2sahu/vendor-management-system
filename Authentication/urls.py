
from django.urls import path,include
from .views import sign_up,login

urlpatterns = [
    path("sign_up",sign_up,name="user_sign_up"),
    path("login",login,name="user_login")
]