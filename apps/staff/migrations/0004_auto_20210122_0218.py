# Generated by Django 3.1.5 on 2021-01-22 02:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0003_auto_20210122_0207'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='staff_type',
            field=models.CharField(blank=True, choices=[('TU', 'Teacher'), ('FO', 'Finance Officer'), ('ASH', 'Assistant School Head'), ('SH', 'School Head'), ('CT', 'Class Teacher')], max_length=200, null=True),
        ),
    ]
