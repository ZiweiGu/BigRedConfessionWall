from django.conf.urls import url
from django.contrib import admin
from django.urls import path

from .views import (
    post_delete_view,
    post_detail_view,
    post_list_view,
    post_update_view,
    postpreference,
)

urlpatterns = [
    path('', post_list_view),
    path('<str:slug>/', post_detail_view),
    path('<str:slug>/edit/', post_update_view),
    path('<str:slug>/delete/', post_delete_view),
    url(r'^(?P<postid>\d+)/preference/(?P<userpreference>\d+)/$', postpreference, name='postpreference'),

]
