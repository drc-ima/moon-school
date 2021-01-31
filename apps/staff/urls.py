from django.urls import path

from apps.staff.views import *

app_name = 'staff'

urlpatterns = [
    path('', staffs, name='list'),
    path('add/', new_staff, name='add'),
    path('mysubjects/', mysubjects, name='mysubjects'),
    path('subject/class/<subject_id>/<class_id>/', subject_class, name='subject-class'),
    path('subject/<subject_id>/class/<class_id>/term/<term_id>/', subject_class_term, name='subject-class-term'),
    path('class/attendance/', class_attendance, name='class-attendance'),
    path('myschedules/', myschedules, name='myschedules'),
]