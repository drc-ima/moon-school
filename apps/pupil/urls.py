from django.urls import path
from .views import *

app_name = 'pupil'


urlpatterns = [
    path('myclass/', myclass, name='myclass'),
    path('class/term/results/<class_id>/<term_id>/', class_term_results, name='class-term-results'),
    path('class/term/attendances/<class_id>/<term_id>/', class_term_attendance, name='class-term-attendances'),
    path('class/pupil/term/<pupil_result_id>/', class_term_pupil, name='class-term-pupil'),
    path('class/pupil/attendance/term/<attendance_id>/<pupil_id>/', class_term_attendance_pupil, name='class-term-attendance-pupil')
]