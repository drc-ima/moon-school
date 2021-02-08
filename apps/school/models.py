import uuid

from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.
from django.utils import timezone


class School(models.Model):
    school_id = models.CharField(blank=True, null=True, max_length=200)
    name = models.CharField(blank=True, null=True, max_length=200)
    slug = models.SlugField(blank=True, null=True, unique=True)
    uuid = models.UUIDField(default=uuid.uuid4, blank=True, null=True, unique=True)
    logo = models.FileField(blank=True, null=True, upload_to='school/')
    domain = models.CharField(blank=True, null=True, max_length=200)
    gps_address = models.CharField(blank=True, null=True, max_length=200)
    phone_number = models.CharField(blank=True, null=True, max_length=200)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, blank=True, null=True,
                                   related_name='institutions')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'school'

    def __str__(self):
        return self.name


class AcademicYear(models.Model):
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, blank=True, null=True,
                                   related_name='academic_years')
    created_at = models.DateTimeField(default=timezone.now)
    is_current = models.BooleanField(blank=True, null=True)
    school_id = models.CharField(blank=True, null=True, max_length=200)

    class Meta:
        db_table = 'academic_year'
        ordering = ['-is_current', '-start_date', '-end_date']

    def __str__(self):
        return f"{self.start_date} - {self.end_date}"


MONTH = {
    ('1', 'January'),
    ('2', 'February'),
    ('3', 'March'),
    ('4', 'April'),
    ('5', 'May'),
    ('6', 'June'),
    ('7', 'July'),
    ('8', 'August'),
    ('9', 'September'),
    ('10', 'October'),
    ('11', 'November'),
    ('12', 'December')
}


DAYS = {
    (1, '1st'),
    (2, '2nd'),
    (3, '3rd'),
    (4, '4th'),
    (5, '5th'),
    (6, '6th'),
    (7, '7th'),
    (8, '8th'),
    (9, '9th'), (10, '10th'), (11, '11th'), (12, '12th'), (13, '13th'), (14, '14th'), (15, '15th'), (16, '16th'),
    (17, '17th'), (18, '18th'), (19, '19th'), (20, '20th'), (21, '21st'), (22, '22nd'), (23, '23rd'), (24, '24th'),
    (25, '25th'), (26, '26th'), (27, '27th'), (28, '28th'), (29, '29th'), (30, '30th'), (31, '31st')
}


class Holiday(models.Model):
    day = models.IntegerField(blank=True, null=True, choices=DAYS)
    month = models.CharField(blank=True, null=True, max_length=255, choices=MONTH)
    title = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                   related_name='holidays', blank=True, null=True)
    school_id = models.CharField(blank=True, null=True, max_length=200)

    def __str__(self):
        return f"{self.day} - {self.get_month_display()}"

    class Meta:
        db_table = 'holiday'
        ordering = ('day',)


class AcademicTerm(models.Model):
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.DO_NOTHING, blank=True, null=True,
                                      related_name='term_academic_year')
    description = models.CharField(max_length=200, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    is_current = models.BooleanField(blank=True, null=True)
    is_promotion = models.BooleanField(blank=True, null=True)
    number_of_weeks = models.IntegerField(blank=True, null=True, default=0)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, blank=True, null=True,
                                   related_name='academic_terms')
    created_at = models.DateTimeField(default=timezone.now)
    school_id = models.CharField(blank=True, null=True, max_length=200)

    class Meta:
        db_table = 'academic_term'
        ordering = ['-is_current', '-start_date', '-end_date']

    def __str__(self):
        return f"{self.start_date} - {self.end_date}"


class Attendance(models.Model):
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.DO_NOTHING, blank=True, null=True,
                                      related_name='attendance_year')
    academic_term = models.ForeignKey(AcademicTerm, on_delete=models.DO_NOTHING, blank=True, null=True,
                                      related_name='attendance_term')
    number_of_days = models.IntegerField(blank=True, null=True, default=0)
    classs = models.ForeignKey('pupil.Class', on_delete=models.DO_NOTHING, blank=True, null=True,
                              related_name='attendance_class')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, blank=True, null=True,
                                   related_name='attendances')
    created_at = models.DateTimeField(default=timezone.now)
    school_id = models.CharField(blank=True, null=True, max_length=200)

    class Meta:
        db_table = 'attendance'

    def __str__(self):
        return f"{self.classs.description}"


class PupilAttendance(models.Model):
    attendance = models.ForeignKey(Attendance, on_delete=models.DO_NOTHING, blank=True, null=True,
                                   related_name='pupil_attendance_attendance')
    date = models.DateField(blank=True, null=True)
    pupil = models.ForeignKey('pupil.Pupil', on_delete=models.DO_NOTHING, blank=True, null=True,
                              related_name='pupil_attendance_pupil')
    status = models.IntegerField(choices={(1, 'Present'), (0, 'Absent')}, blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, blank=True, null=True,
                                   related_name='pupil_attendances')
    created_at = models.DateTimeField(default=timezone.now)
    school_id = models.CharField(blank=True, null=True, max_length=200)

    class Meta:
        db_table = 'pupil_attendance'

    def __str__(self):
        return f"{self.date} - {self.pupil.full_name()}"


class Result(models.Model):
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.DO_NOTHING, blank=True, null=True,
                                      related_name='performance_year')
    academic_term = models.ForeignKey(AcademicTerm, on_delete=models.DO_NOTHING, blank=True, null=True,
                                      related_name='performance_term')
    status = models.IntegerField(choices={(0, 'Opened'), (1, 'Completed')}, blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, blank=True, null=True,
                                   related_name='results')
    created_at = models.DateTimeField(default=timezone.now)
    school_id = models.CharField(blank=True, null=True, max_length=200)

    class Meta:
        db_table = 'result'

    def __str__(self):
        return f"{self.academic_term.description} - {self.academic_year}"


class PupilResult(models.Model):
    result = models.ForeignKey(Result, on_delete=models.DO_NOTHING, blank=True, null=True,
                               related_name='pupil_result_result')
    classe = models.ForeignKey('pupil.Class', on_delete=models.DO_NOTHING, blank=True, null=True,
                               related_name='pupil_result_class')
    pupil = models.ForeignKey('pupil.Pupil', on_delete=models.DO_NOTHING, blank=True, null=True,
                              related_name='pupil_result_pupil')
    comments = models.TextField(blank=True, null=True)
    final_grade = models.CharField(default='', max_length=10, blank=True, null=True)
    final_score = models.DecimalField(decimal_places=2, max_digits=10, default=0.00, blank=True, null=True)
    status = models.IntegerField(choices={(0, 'Opened'), (1, 'Completed')}, blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, blank=True, null=True,
                                   related_name='pupil_results')
    created_at = models.DateTimeField(default=timezone.now)
    school_id = models.CharField(blank=True, null=True, max_length=200)

    class Meta:
        db_table = 'pupil_result'
        # ordering = ('-grade',)

    def __str__(self):
        return f"{self.pupil.full_name()} - {self.result}"


class PupilResultSubject(models.Model):
    subject = models.ForeignKey('staff.Subject', on_delete=models.DO_NOTHING, blank=True, null=True,
                                related_name='pupil_result_subject_subject')
    pupil_result = models.ForeignKey(PupilResult, on_delete=models.DO_NOTHING, blank=True, null=True,
                                     related_name='pupil_result_subject_pupil_result')
    result = models.ForeignKey(Result, on_delete=models.DO_NOTHING, blank=True, null=True,
                                     related_name='pupil_result_subject_result')
    class_score = models.DecimalField(decimal_places=2, max_digits=10, default=0.00, blank=True, null=True)
    exam_score = models.DecimalField(decimal_places=2, max_digits=10, default=0.00, blank=True, null=True)
    pupil = models.ForeignKey('pupil.Pupil', on_delete=models.DO_NOTHING, blank=True, null=True,
                              related_name='pupil_result_subject_pupil')
    grade = models.CharField(max_length=10, blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, blank=True, null=True,
                                   related_name='pupil_result_subjects')
    created_at = models.DateTimeField(default=timezone.now)
    school_id = models.CharField(blank=True, null=True, max_length=200)

    class Meta:
        db_table = 'pupil_result_subject'
        ordering = ['subject__description']

    def __str__(self):
        return f"{self.subject.description} - {self.pupil_result}"

    def total_score(self):
        return self.class_score + self.exam_score


class GradeScheme(models.Model):
    from_score = models.DecimalField(decimal_places=2, max_digits=10, default=0.00, blank=True, null=True)
    to_score = models.DecimalField(decimal_places=2, max_digits=10, default=0.00, blank=True, null=True)
    grade = models.CharField(blank=True, null=True, max_length=10)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, blank=True, null=True,
                                   related_name='grade_schemes')
    created_at = models.DateTimeField(default=timezone.now)
    school_id = models.CharField(blank=True, null=True, max_length=200)

    class Meta:
        db_table = 'grade_scheme'
        ordering = ['-from_score', '-to_score', '-grade']

    def __str__(self):
        return f"{self.from_score} - {self.to_score} | {self.grade}"


class PassGrade(models.Model):
    score = models.DecimalField(decimal_places=2, max_digits=10, default=0.00, blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, blank=True, null=True,
                                   related_name='pass_grades')
    created_at = models.DateTimeField(default=timezone.now)
    school_id = models.CharField(blank=True, null=True, max_length=200)

    class Meta:
        db_table = 'pass_grade'
        # ordering = ['-from_score', '-to_score', '-grade']

    def __str__(self):
        return f"{self.score}"


@receiver(post_save, sender=AcademicYear)
def current_year(sender, created, instance, *args, **kwargs):
    school_id = instance.school_id
    if instance.is_current == True:
        AcademicYear.objects.filter(school_id=school_id).exclude(id=instance.id).update(is_current=False)


@receiver(post_save, sender=AcademicTerm)
def current_term(sender, created, instance, *args, **kwargs):
    school_id = instance.school_id
    if instance.is_current:
        AcademicTerm.objects.filter(school_id=school_id).exclude(id=instance.id).update(is_current=False)


@receiver(post_save, sender=AcademicTerm)
def promotion_term(sender, created, instance, *args, **kwargs):
    school_id = instance.school_id
    academic_year = instance.academic_year

    if instance.is_promotion:
        AcademicTerm.objects.filter(school_id=school_id, academic_year=academic_year).exclude(id=instance.id).update(is_promotion=False)