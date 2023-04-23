from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("machines/<str:activity>", views.machines, name="machines"),
    path("data", views.dataAPI, name="data"),
    path("request", views.request, name="request"),
    path("update", views.updateAPI, name="update")
   
]