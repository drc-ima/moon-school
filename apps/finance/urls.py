from django.urls import path
from .views import *

app_name = 'finance'


urlpatterns = [
    path('setup/', fee_setup, name='setup'),
    path('schedules/<term_id>/', fee_schedules, name='schedules'),
    path('schedule/add/<term_id>/', new_schedule, name='schedule-add'),
    path('payments/', fee_payments, name='payments'),
    path('payment/new/', new_payment, name='payment-new'),
    path('payment/receipt/<receipt_id>/', receipt_view, name='payment-receipt'),
    path('class-pupils/<class_id>/', class_pupils, name='class-pupils')
]