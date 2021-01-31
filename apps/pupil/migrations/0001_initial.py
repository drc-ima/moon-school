# Generated by Django 3.1.5 on 2021-01-22 02:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('staff', '0003_auto_20210122_0207'),
    ]

    operations = [
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, max_length=200, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('school_id', models.CharField(blank=True, max_length=200, null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='classes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'class',
            },
        ),
        migrations.CreateModel(
            name='Pupil',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=200, null=True)),
                ('moon_id', models.CharField(blank=True, max_length=200, null=True)),
                ('pupil_id', models.CharField(blank=True, max_length=200, null=True)),
                ('middle_name', models.CharField(blank=True, max_length=200, null=True)),
                ('last_name', models.CharField(blank=True, max_length=200, null=True)),
                ('previous_school', models.CharField(blank=True, max_length=500, null=True)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('guardian', models.CharField(blank=True, choices=[('O', 'Other'), ('P', 'Parent')], max_length=200, null=True)),
                ('mother_name', models.CharField(blank=True, max_length=200, null=True)),
                ('father_name', models.CharField(blank=True, max_length=200, null=True)),
                ('other_name', models.CharField(blank=True, max_length=200, null=True)),
                ('guardian_contact', models.CharField(blank=True, max_length=200, null=True)),
                ('address', models.CharField(blank=True, max_length=300, null=True)),
                ('profile', models.FileField(blank=True, null=True, upload_to='pupil/')),
                ('account_activated', models.BooleanField(blank=True, default=False, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('school_id', models.CharField(blank=True, max_length=200, null=True)),
                ('classs', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='pupil_class', to='pupil.class')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='pupils', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'pupil',
            },
        ),
        migrations.CreateModel(
            name='PupilClass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('school_id', models.CharField(blank=True, max_length=200, null=True)),
                ('classe', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='pupil_class_class', to='pupil.class')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='pupil_classes', to=settings.AUTH_USER_MODEL)),
                ('pupil', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='pupil_class_pupil', to='pupil.pupil')),
            ],
            options={
                'db_table': 'pupil_class',
            },
        ),
        migrations.CreateModel(
            name='ClassSubject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('school_id', models.CharField(blank=True, max_length=200, null=True)),
                ('classe', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='class_subject_class', to='pupil.class')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='class_subjects', to=settings.AUTH_USER_MODEL)),
                ('subject', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='class_subject_subject', to='staff.subject')),
            ],
            options={
                'db_table': 'class_subject',
            },
        ),
    ]
