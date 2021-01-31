from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(FeeSchedule)
admin.site.register(FeeItem)
admin.site.register(FeeScheduleItem)
admin.site.register(StudentFee)
admin.site.register(StudentPayment)
admin.site.register(Receipt)