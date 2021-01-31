from django.conf import settings
from django.db import models

# Create your models here.
from django.utils import timezone


class Class(models.Model):
    description = models.CharField(max_length=200, blank=True, null=True)
    teacher = models.ForeignKey('staff.Staff', on_delete=models.DO_NOTHING, blank=True, null=True,
                                related_name='class_teacher')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, blank=True, null=True,
                                   related_name='classes')
    created_at = models.DateTimeField(default=timezone.now)
    school_id = models.CharField(blank=True, null=True, max_length=200)

    class Meta:
        db_table = 'class'

    def __str__(self):
        return f"{self.description}"


class ClassSubject(models.Model):
    classe = models.ForeignKey(Class, on_delete=models.DO_NOTHING, blank=True, null=True,
                               related_name='class_subject_class')
    subject = models.ForeignKey('staff.Subject', on_delete=models.DO_NOTHING, blank=True, null=True,
                                related_name='class_subject_subject')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, blank=True, null=True,
                                   related_name='class_subjects')
    created_at = models.DateTimeField(default=timezone.now)
    school_id = models.CharField(blank=True, null=True, max_length=200)

    class Meta:
        db_table = 'class_subject'

    def __str__(self):
        return f"{self.classe.description} - {self.subject.description}"


GUARDIAN = {
    ('P', 'Parent'),
    ('O', 'Other')
}


GENDER = {
    ('male', 'Male'),
    ('female', 'Female')
}

STATUS = {
    ('D', 'Day'),
    ('FD', 'Fresh Day'),
    ('B', 'Boarder'),
    ('FB', 'Fresh Boarder')
}


class Pupil(models.Model):
    first_name = models.CharField(max_length=200, blank=True, null=True)
    # moon_id = models.CharField(max_length=200, blank=True, null=True)
    pupil_id = models.CharField(max_length=200, blank=True, null=True)
    middle_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    classs = models.ForeignKey(Class, on_delete=models.DO_NOTHING, blank=True, null=True,
                              related_name='pupil_class')
    previous_school = models.CharField(max_length=500, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    guardian = models.CharField(max_length=200, blank=True, null=True, choices=GUARDIAN)
    mother_name = models.CharField(max_length=200, blank=True, null=True)
    father_name = models.CharField(max_length=200, blank=True, null=True)
    other_name = models.CharField(max_length=200, blank=True, null=True)
    guardian_contact = models.CharField(max_length=200, blank=True, null=True)
    address = models.CharField(max_length=300, blank=True, null=True)
    profile = models.FileField(upload_to='pupil/', blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True, choices=STATUS)
    account_activated = models.BooleanField(default=False, blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, blank=True, null=True,
                                   related_name='pupils')
    created_at = models.DateTimeField(default=timezone.now)
    school_id = models.CharField(blank=True, null=True, max_length=200)
    gender = models.CharField(blank=True, null=True, max_length=200, choices=GENDER)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, blank=True, null=True,
                             related_name='pupil_user')

    class Meta:
        db_table = 'pupil'

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name()


class PupilClass(models.Model):
    pupil = models.ForeignKey(Pupil, on_delete=models.DO_NOTHING, blank=True, null=True,
                              related_name='pupil_class_pupil')
    classe = models.ForeignKey(Class, on_delete=models.DO_NOTHING, blank=True, null=True,
                               related_name='pupil_class_class')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, blank=True, null=True,
                                   related_name='pupil_classes')
    created_at = models.DateTimeField(default=timezone.now)
    school_id = models.CharField(blank=True, null=True, max_length=200)

    class Meta:
        db_table = 'pupil_class'

    def full_name(self):
        return f"{self.pupil} {self.classe}"

    def __str__(self):
        return self.full_name()