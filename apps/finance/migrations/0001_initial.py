# Generated by Django 3.1.5 on 2021-01-27 00:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('school', '0006_auto_20210127_0025'),
        ('pupil', '0006_auto_20210127_0025'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeeItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.CharField(blank=True, max_length=200, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('school_id', models.CharField(blank=True, max_length=200, null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='fee_items', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'fee_item',
            },
        ),
        migrations.CreateModel(
            name='FeeSchedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('school_id', models.CharField(blank=True, max_length=200, null=True)),
                ('academic_term', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='fee_schedule_term', to='school.academicterm')),
                ('classe', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='fee_schedule_classe', to='pupil.class')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='fee_schedules', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'fee_schedule',
            },
        ),
        migrations.CreateModel(
            name='StudentFee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('arrears', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True)),
                ('remaining', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True)),
                ('amount_paid', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True)),
                ('amount_to_pay', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True)),
                ('fully_paid', models.BooleanField(blank=True, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('school_id', models.CharField(blank=True, max_length=200, null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='student_fees', to=settings.AUTH_USER_MODEL)),
                ('fee_schedule', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='student_fee_fee_schedule', to='finance.feeschedule')),
                ('pupil', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='student_fee_pupil', to='pupil.pupil')),
            ],
            options={
                'db_table': 'student_fee',
            },
        ),
        migrations.CreateModel(
            name='StudentPayment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True)),
                ('payment_id', models.CharField(blank=True, max_length=200, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('school_id', models.CharField(blank=True, max_length=200, null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='payments', to=settings.AUTH_USER_MODEL)),
                ('student_fee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='payment_student_fee', to='finance.studentfee')),
            ],
            options={
                'db_table': 'student_payment',
            },
        ),
        migrations.CreateModel(
            name='Receipt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('receipt_id', models.CharField(blank=True, max_length=100, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('school_id', models.CharField(blank=True, max_length=200, null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='receipts', to=settings.AUTH_USER_MODEL)),
                ('student_payment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='receipt_student_payment', to='finance.studentpayment')),
            ],
            options={
                'db_table': 'receipt',
            },
        ),
        migrations.CreateModel(
            name='FeeScheduleItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True)),
                ('student_status', models.CharField(blank=True, choices=[('D', 'Day'), ('FD', 'Fresh Day'), ('B', 'Boarder'), ('FB', 'Fresh Boarder')], max_length=200, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('school_id', models.CharField(blank=True, max_length=200, null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='fee_schedule_items', to=settings.AUTH_USER_MODEL)),
                ('fee_item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='item_fee_item', to='finance.feeitem')),
                ('fee_schedule', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='item_fee_schedule', to='finance.feeschedule')),
            ],
            options={
                'db_table': 'fee_schedule_item',
            },
        ),
    ]
