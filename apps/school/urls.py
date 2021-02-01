from django.urls import path
from .views import *

app_name = 'school'


urlpatterns = [
    path('', myschool, name='myschool'),
    path('add/', SchoolSignup.as_view()),
    path('management/', management, name='management'),
    path('management/class/<id>/', class_detail, name='management-class'),
    path('management/subject/<id>/', subject_detail, name='management-subject'),
    path('academics/', academics, name='academics'),
    path('academic/<id>/', academic_details, name='academic-details'),
    path('academic/term/<id>/', term_details, name='academic-term'),
    path('academic/results/class/<id>/', class_results, name='academic-results-class'),
    path('academic/attendances/<attendance_id>/', class_attendances, name='academic-attendances'),
    path('pupils/', pupils, name='pupils'),
    path('pupil/add/', new_pupil, name='pupil-add'),
]