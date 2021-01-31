from django.conf import settings
from django.db import models
import uuid
# Create your models here.
from django.utils import timezone

STAFF_TYPE = {
    ('SH', 'School Head'),
    ('ASH', 'Assistant School Head'),
    ('TU', 'Teacher'),
    ('CT', 'Class Teacher'),
    ('FO', 'Finance Officer'),
}


class Staff(models.Model):
    staff_type = models.CharField(max_length=200, blank=True, null=True, choices=STAFF_TYPE)
    # moon_id = models.CharField(max_length=200, blank=True, null=True)
    staff_id = models.CharField(max_length=200, blank=True, null=True)
    first_name = models.CharField(max_length=200, blank=True, null=True)
    middle_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    date_employed = models.DateField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, blank=True, null=True,
                                   related_name='staffs')
    created_at = models.DateTimeField(default=timezone.now)
    slug = models.SlugField(blank=True, null=True, unique=True)
    uuid = models.UUIDField(default=uuid.uuid4, blank=True, null=True, unique=True)
    account_activated = models.BooleanField(default=False, blank=True, null=True)
    profile = models.FileField(upload_to='staff/', blank=True, null=True)
    school_id = models.CharField(blank=True, null=True, max_length=200)
    gender = models.CharField(max_length=200, blank=True, null=True, choices={('male', 'Male'), ('female', 'Female'), ('other', 'Others')})
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, blank=True, null=True,
                             related_name='staff_user')

    class Meta:
        db_table = 'staff'

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name()


class Subject(models.Model):
    description = models.CharField(max_length=200, blank=True, null=True)
    subject_code = models.CharField(max_length=200, blank=True, null=True)
    teacher = models.ForeignKey(Staff, on_delete=models.DO_NOTHING, null=True, blank=True,
                                related_name='subject_teacher')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, blank=True, null=True,
                                   related_name='subjects')
    created_at = models.DateTimeField(default=timezone.now)
    school_id = models.CharField(blank=True, null=True, max_length=200)

    class Meta:
        db_table = 'subject'

    def __str__(self):
        return self.description


class SubjectTeacher(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.DO_NOTHING, blank=True, null=True,
                                related_name='subject_teacher_subject')
    teacher = models.ForeignKey(Staff, on_delete=models.DO_NOTHING, blank=True, null=True,
                                related_name='subject_teacher_teacher')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, blank=True, null=True,
                                   related_name='subject_teachers')
    created_at = models.DateTimeField(default=timezone.now)
    school_id = models.CharField(blank=True, null=True, max_length=200)

    class Meta:
        db_table = 'subject_teacher'

    def __str__(self):
        return f"{self.subject.description} - {self.teacher.full_name()}"
