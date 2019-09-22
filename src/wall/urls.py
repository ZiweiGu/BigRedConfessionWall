from django.conf.urls import url
from django.contrib import admin
from django.urls import path

from .views import (
    post_delete_view,
    post_detail_view,
    post_list_view,
    post_update_view,
    postpreference,
    add_comment_to_post,
    comment_approve,
    comment_remove, 
)

urlpatterns = [
    path('', post_list_view),
    path('<str:slug>/', post_detail_view),
    path('<str:slug>/edit/', post_update_view),
    path('<str:slug>/delete/', post_delete_view),
    url(r'^(?P<postid>\d+)/preference/(?P<userpreference>\d+)/$', postpreference, name='postpreference'),
    path('<str:slug>/comment/', add_comment_to_post, name='add_comment_to_post'),
    path('<str:slug>/comment/approve/', comment_approve, name='comment_approve'),
    path('<str:slug>/comment/remove/', comment_remove, name='comment_remove'),
]
