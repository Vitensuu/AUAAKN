"""
URL configuration for rentproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from rentapp.views import main_page, create_post, edit_post, post_detail, post_list, post_delete, book_property, add_rating,toggle_favorite, search_posts
from django.urls import path
from user.views import registration, userLogin, userLogout, activate
from messaging.views import notification_list, mark_as_read, delete_notification
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('search/', search_posts, name='search_posts'),
    path('', main_page, name='main_page'),
    path ('rents/', post_list, name='post_list'),
    path ('createpost/', create_post, name='create_post'),
    path ('<int:pid>/edit/', edit_post, name='edit_post'),
    path ('<int:pid>/deleate/', post_delete, name='post_delete'),
    path ('<int:post_id>/', post_detail, name='post_detail'),
    path ('book_property/<int:post_id>/', book_property , name='book_property'),
    path ('add_rating/<int:post_id>/', add_rating, name='add_rating'),
    path ('add_favorite/<int:post_id>/', toggle_favorite, name='add_favorite'),
    path('registration/', registration, name='register'),
    path('login/', userLogin, name='login'),
    path('logout/', userLogout, name='logout'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('book/<int:post_id>/', book_property, name='book_property'),
    path('notifications/', notification_list, name='notification_list'),
    path('notifications/read/<int:notification_id>/', mark_as_read, name='mark_as_read'),
    path('notifications/delete/<int:notification_id>/', delete_notification, name='delete_notification'),
    path('wallet/', include(('wallet.urls', 'wallet'), namespace='wallet')),



]

