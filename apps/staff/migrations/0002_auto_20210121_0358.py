# Generated by Django 3.1.5 on 2021-01-21 03:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='staff',
            name='moon_id',
        ),
        migrations.AlterField(
            model_name='staff',
            name='staff_type',
            field=models.CharField(blank=True, choices=[('SH', 'School Head'), ('FO', 'Finance Officer'), ('CT', 'Class Teacher'), ('TU', 'Teacher'), ('ASH', 'Assistant School Head')], max_length=200, null=True),
        ),
    ]
