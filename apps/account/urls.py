from django.urls import path
from .views import *
app_name = 'account'


urlpatterns = [
    path('register/school/', signup_school, name='register-school'),
    path('register/user/', signup_user, name='register-user'),
    path('', dashboard, name='dashboard'),
    path('logout/', user_logout, name='logout')
]