# Generated by Django 3.1.5 on 2021-01-24 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0007_auto_20210123_0149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='gender',
            field=models.CharField(blank=True, choices=[('female', 'Female'), ('other', 'Others'), ('male', 'Male')], max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='staff',
            name='staff_type',
            field=models.CharField(blank=True, choices=[('TU', 'Teacher'), ('CT', 'Class Teacher'), ('FO', 'Finance Officer'), ('SH', 'School Head'), ('ASH', 'Assistant School Head')], max_length=200, null=True),
        ),
    ]
