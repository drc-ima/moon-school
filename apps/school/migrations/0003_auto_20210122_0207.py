# Generated by Django 3.1.5 on 2021-01-22 02:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('pupil', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('staff', '0003_auto_20210122_0207'),
        ('school', '0002_auto_20210120_2124'),
    ]

    operations = [
        migrations.CreateModel(
            name='AcademicTerm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, max_length=200, null=True)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('is_current', models.BooleanField(blank=True, null=True)),
                ('number_of_weeks', models.IntegerField(blank=True, default=0, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('school_id', models.CharField(blank=True, max_length=200, null=True)),
            ],
            options={
                'db_table': 'academic_term',
            },
        ),
        migrations.CreateModel(
            name='AcademicYear',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_current', models.BooleanField(blank=True, null=True)),
                ('school_id', models.CharField(blank=True, max_length=200, null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='academic_years', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'academic_year',
            },
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_of_days', models.IntegerField(blank=True, default=0, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('school_id', models.CharField(blank=True, max_length=200, null=True)),
                ('academic_term', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='attendance_term', to='school.academicterm')),
                ('academic_year', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='attendance_year', to='school.academicyear')),
                ('classs', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='attendance_class', to='pupil.class')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='attendances', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'attendance',
            },
        ),
        migrations.CreateModel(
            name='PupilResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comments', models.TextField(blank=True, null=True)),
                ('final_grade', models.CharField(blank=True, max_length=10, null=True)),
                ('final_score', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True)),
                ('status', models.IntegerField(blank=True, choices=[(0, 'Opened'), (1, 'Completed')], null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('school_id', models.CharField(blank=True, max_length=200, null=True)),
                ('classe', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='pupil_result_class', to='pupil.class')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='pupil_results', to=settings.AUTH_USER_MODEL)),
                ('pupil', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='pupil_result_pupil', to='pupil.pupil')),
            ],
            options={
                'db_table': 'pupil_result',
            },
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(blank=True, choices=[(0, 'Opened'), (1, 'Completed')], null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('school_id', models.CharField(blank=True, max_length=200, null=True)),
                ('academic_term', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='performance_term', to='school.academicterm')),
                ('academic_year', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='performance_year', to='school.academicyear')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='results', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'result',
            },
        ),
        migrations.CreateModel(
            name='PupilResultSubject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_score', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True)),
                ('exam_score', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True)),
                ('grade', models.CharField(blank=True, max_length=10, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('school_id', models.CharField(blank=True, max_length=200, null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='pupil_result_subjects', to=settings.AUTH_USER_MODEL)),
                ('pupil', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='pupil_result_subject_pupil', to='pupil.pupil')),
                ('pupil_result', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='pupil_result_subject_pupil_result', to='school.pupilresult')),
                ('subject', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='pupil_result_subject_subject', to='staff.subject')),
            ],
            options={
                'db_table': 'pupil_result_subject',
            },
        ),
        migrations.AddField(
            model_name='pupilresult',
            name='result',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='pupil_result_result', to='school.result'),
        ),
        migrations.CreateModel(
            name='PupilAttendance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, null=True)),
                ('status', models.IntegerField(blank=True, choices=[(0, 'Absent'), (1, 'Present')], null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('school_id', models.CharField(blank=True, max_length=200, null=True)),
                ('attendance', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='pupil_attendance_attendance', to='school.attendance')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='pupil_attendances', to=settings.AUTH_USER_MODEL)),
                ('pupil', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='pupil_attendance_pupil', to='pupil.pupil')),
            ],
            options={
                'db_table': 'pupil_attendance',
            },
        ),
        migrations.CreateModel(
            name='Holiday',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.IntegerField(blank=True, choices=[(26, '26th'), (29, '29th'), (27, '27th'), (25, '25th'), (4, '4th'), (17, '17th'), (1, '1st'), (31, '31st'), (3, '3rd'), (6, '6th'), (5, '5th'), (24, '24th'), (13, '13th'), (9, '9th'), (23, '23rd'), (11, '11th'), (14, '14th'), (19, '19th'), (7, '7th'), (12, '12th'), (30, '30th'), (2, '2nd'), (21, '21st'), (28, '28th'), (18, '18th'), (10, '10th'), (8, '8th'), (16, '16th'), (20, '20th'), (22, '22nd'), (15, '15th')], null=True)),
                ('month', models.CharField(blank=True, choices=[('6', 'June'), ('3', 'March'), ('9', 'September'), ('8', 'August'), ('2', 'February'), ('4', 'April'), ('12', 'December'), ('1', 'January'), ('7', 'July'), ('5', 'May'), ('11', 'November'), ('10', 'October')], max_length=255, null=True)),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('school_id', models.CharField(blank=True, max_length=200, null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='holidays', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'holiday',
                'ordering': ('day',),
            },
        ),
        migrations.CreateModel(
            name='GradeScheme',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_score', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True)),
                ('to_score', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True)),
                ('grade', models.CharField(blank=True, max_length=10, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('school_id', models.CharField(blank=True, max_length=200, null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='grade_schemes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'grade_scheme',
            },
        ),
        migrations.AddField(
            model_name='academicterm',
            name='academic_year',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='term_academic_year', to='school.academicyear'),
        ),
        migrations.AddField(
            model_name='academicterm',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='academic_terms', to=settings.AUTH_USER_MODEL),
        ),
    ]
