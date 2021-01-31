# Generated by Django 3.1.5 on 2021-01-22 04:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('staff', '0005_auto_20210122_0304'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='staff_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='staff',
            name='gender',
            field=models.CharField(blank=True, choices=[('female', 'Female'), ('other', 'Others'), ('male', 'Male')], max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='staff',
            name='staff_type',
            field=models.CharField(blank=True, choices=[('TU', 'Teacher'), ('FO', 'Finance Officer'), ('SH', 'School Head'), ('CT', 'Class Teacher'), ('ASH', 'Assistant School Head')], max_length=200, null=True),
        ),
    ]
