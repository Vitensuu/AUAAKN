from django.urls import path
from .views import *

urlpatterns = [
    path('', Post_list, name='post_list'),
    path('<int:pid>/', DetailsPage, name='post_details'),
    path('add/', Add_post, name='add_post'),
    path('<int:pid>/edit/', Edit_post, name='edit_post'),
    path('<int:pid>/delete/', post_delete, name='post_delete'),

]