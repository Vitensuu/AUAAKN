from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path, re_path
from user.views import registration, userLogin, userLogout, activate
urlpatterns = [
    ]