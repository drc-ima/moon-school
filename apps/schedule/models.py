from django.conf import settings
from django.db import models

# Create your models here.
from django.utils import timezone


class ClassSchedule(models.Model):
    classe = models.ForeignKey('pupil.Class', on_delete=models.DO_NOTHING, blank=True, null=True,
                               related_name='class_schedule_class')
    academic_term = models.ForeignKey('school.AcademicTerm', on_delete=models.DO_NOTHING, blank=True, null=True,
                                      related_name='class_schedule_term')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, blank=True, null=True,
                                   related_name='class_schedules')
    created_at = models.DateTimeField(default=timezone.now)
    school_id = models.CharField(blank=True, null=True, max_length=200)

    class Meta:
        db_table = 'class_schedule'

    def __str__(self):
        return f"{self.classe}"


DAYS = {
    (0, 'Mondays'),
    (1, 'Tuesdays'),
    (2, 'Wednesdays'),
    (3, 'Thursdays'),
    (4, 'Fridays')
}


class ClassScheduleActivity(models.Model):
    class_schedule = models.ForeignKey(ClassSchedule, on_delete=models.DO_NOTHING, blank=True, null=True,
                                       related_name='activity_class_schedule')
    day = models.IntegerField(blank=True, null=True, choices=DAYS)
    hour = models.CharField(max_length=10, blank=True, null=True)
    subject = models.ForeignKey('staff.Subject', on_delete=models.DO_NOTHING, blank=True, null=True,
                                related_name='activity_subject')
    is_subject = models.BooleanField(blank=True, null=True)
    item = models.CharField(blank=True, null=True, max_length=200)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, blank=True, null=True,
                                   related_name='class_schedule_activities')
    created_at = models.DateTimeField(default=timezone.now)
    school_id = models.CharField(blank=True, null=True, max_length=200)

    class Meta:
        db_table = 'class_schedule_activity'

    def __str__(self):
        return f"{self.subject if self.is_subject else self.item} - {self.hour} - {self.get_day_display()}"
