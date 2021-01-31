from django.urls import path
from .views import *

app_name = 'schedule'

urlpatterns = [
    path('class/<class_id>/<term_id>/', class_schedules, name='class')
]