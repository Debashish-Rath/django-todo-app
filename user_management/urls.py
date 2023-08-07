from django.urls import path
from .views import *

urlpatterns = [

    # Dashboard URL
    path("", index, name='home'),


    # Create, Update, Delete URLs
    path("add_todo/", add_todo_item, name='add_todo'),
    path("delete_todo/<int:todo_id>", delete_todo_item, name='delete_todo'),
    path("update_todo/<int:todo_id>", update_todo_item, name='update_todo'),


    # User Register, Login, Logout URLs
    path("register", register, name='register'),
    path("login", login_user, name='login_user'),
    path("logout", logout_user, name='logout_user')
]
