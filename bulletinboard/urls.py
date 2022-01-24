"""
The whole route urls of Bulletinboard django project
"""

from django.urls import path
from django.urls.conf import re_path
from . import views

urlpatterns = [
    re_path(r"^accounts/login/$", views.user_login, name="user_login"),
    path("", views.index, name="index"),
    path("post/create/", views.postCreate, name="post-create"),
    path("post/<int:pk>/", views.postUpdate, name="post-update"),
    path("post/detail/", views.post_detail, name="post-detail"),
    path("post/delete/confirm/", views.post_delete_confirm,
         name="post-delete-confirm"),
    path("post/delete/", views.post_delete, name="post-delete"),
    path("users/", views.userList, name="user-list"),
    path("user/create/", views.userCreate, name="user-create"),
    path("profile/", views.userProfile, name="user-profile"),
    path("user/<int:pk>/", views.userUpdate, name="user-update"),
    path("user/detail/", views.user_detail, name="user-detail"),
    path("user/delete/confirm/", views.user_delete_confirm,
         name="user-delete-confirm"),
    path("user/delete/", views.user_delete, name="user-delete"),
    path("csv/import/", views.csv_import, name="csv-import"),
    path("post/list/download", views.download_post_list_csv,
         name="post-list-download"),
    path("password-reset/", views.user_password_reset, name="password-reset"),
    re_path(r"^accounts/register/$", views.signup, name="create_account"),
]
