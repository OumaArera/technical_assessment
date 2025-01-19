from django.urls import path # type: ignore
from customers.views.user_view import UserView
from customers.views.login_view import LoginView

urlpatterns=[
    path(
        'users', 
        UserView.as_view(), 
        name='users'
    ),
    path(
        'users/<int:user_id>', 
        UserView.as_view(), 
        name='user-details'
    ),
    path(
        'auth', 
        LoginView.as_view(), 
        name='auth'
    ),
]