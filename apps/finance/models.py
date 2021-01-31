from django.conf import settings
from django.db import models

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from apps.pupil.models import Pupil


STATUS = {
    ('B', 'Boarders'),
    ('D', 'Days'),
    ('FD', 'Fresh Day'),
    ('FB', 'Fresh Boarder')
}


class FeeSchedule(models.Model):
    academic_term = models.ForeignKey('school.AcademicTerm', on_delete=models.DO_NOTHING, blank=True, null=True,
                                      related_name='fee_schedule_term')
    classe = models.ForeignKey('pupil.Class', on_delete=models.DO_NOTHING, blank=True, null=True,
                               related_name='fee_schedule_classe')
    amount = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)
    student_status = models.CharField(max_length=200, blank=True, null=True, choices=STATUS)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, blank=True, null=True,
                                   related_name='fee_schedules')
    created_at = models.DateTimeField(default=timezone.now)
    school_id = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'fee_schedule'

    def __str__(self):
        return f"{self.classe} - {self.amount} - {self.academic_term}"


class FeeItem(models.Model):
    item = models.CharField(max_length=200, blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, blank=True, null=True,
                                   related_name='fee_items')
    created_at = models.DateTimeField(default=timezone.now)
    school_id = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'fee_item'

    def __str__(self):
        return f"{self.item}"


class FeeScheduleItem(models.Model):
    fee_schedule = models.ForeignKey(FeeSchedule, on_delete=models.DO_NOTHING, blank=True, null=True,
                                     related_name='item_fee_schedule')
    fee_item = models.ForeignKey(FeeItem, on_delete=models.DO_NOTHING, blank=True, null=True,
                                 related_name='item_fee_item')
    amount = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True, default=0.00)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, blank=True, null=True,
                                   related_name='fee_schedule_items')
    created_at = models.DateTimeField(default=timezone.now)
    school_id = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'fee_schedule_item'

    def __str__(self):
        return f"{self.fee_item} - {self.amount} - {self.fee_schedule}"


class StudentFee(models.Model):
    fee_schedule = models.ForeignKey(FeeSchedule, on_delete=models.DO_NOTHING, blank=True, null=True,
                                     related_name='student_fee_fee_schedule')
    pupil = models.ForeignKey('pupil.Pupil', on_delete=models.DO_NOTHING, blank=True, null=True,
                              related_name='student_fee_pupil')
    arrears = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True, default=0.00)
    remaining = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True, default=0.00)
    balance = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True, default=0.00)
    amount_paid =  models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True, default=0.00)
    amount_to_pay = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True, default=0.00)
    fully_paid = models.BooleanField(blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, blank=True, null=True,
                                   related_name='student_fees')
    created_at = models.DateTimeField(default=timezone.now)
    school_id = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'student_fee'

    def __str__(self):
        return f"{self.pupil} - {self.fee_schedule.amount} - {self.amount_paid}"


class StudentPayment(models.Model):
    student_fee = models.ForeignKey(StudentFee, on_delete=models.DO_NOTHING, blank=True, null=True,
                                   related_name='payment_student_fee')
    amount = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True, default=0.00)
    payment_id = models.CharField(max_length=200, blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, blank=True, null=True,
                                   related_name='payments')
    created_at = models.DateTimeField(default=timezone.now)
    school_id = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'student_payment'

    def __str__(self):
        return f"{self.student_fee.pupil} - {self.amount}"


class Receipt(models.Model):
    receipt_id = models.CharField(max_length=100, blank=True, null=True)
    student_payment = models.ForeignKey(StudentPayment, on_delete=models.DO_NOTHING, blank=True, null=True,
                                        related_name='receipt_student_payment')
    status = models.IntegerField(choices={(0, 'Part Payment'), (1, 'Full Payment')}, blank=True, null=True)
    words = models.CharField(max_length=300, blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, blank=True, null=True,
                                   related_name='receipts')
    created_at = models.DateTimeField(default=timezone.now)
    school_id = models.CharField(max_length=200, blank=True, null=True)
    last_printed = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'receipt'

    def __str__(self):
        return f"{self.receipt_id}"


@receiver(post_save, sender=FeeSchedule)
def student_fee(sender, created, instance, *args, **kwargs):
    if instance.amount:
        school_id = instance.school_id
        classe = instance.classe
        students = Pupil.objects.filter(school_id=school_id, classs=classe)

        for student in students:
            try:
                old_formal_sf = StudentFee.objects.get(
                    pupil=student,
                    fee_schedule__academic_term__is_current=True,
                    school_id=school_id,
                    fully_paid=False,
                    pupil__status=instance.student_status
                )

                nsf = StudentFee(
                    fee_schedule=instance,
                    pupil=student,
                    arrears=old_formal_sf.remaining,
                    amount_to_pay=old_formal_sf.remaining + instance.amount - old_formal_sf.balance,
                    school_id=school_id,
                    created_by=instance.created_by
                )

                nsf.save()
            except StudentFee.DoesNotExist:
                if instance.student_status == student.status:
                    nsf = StudentFee(
                        fee_schedule=instance,
                        pupil=student,
                        # arrears=old_formal_sf.remaining,
                        amount_to_pay=instance.amount,
                        school_id=school_id,
                        created_by=instance.created_by
                    )

                    nsf.save()