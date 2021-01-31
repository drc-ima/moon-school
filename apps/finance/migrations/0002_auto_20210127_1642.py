# Generated by Django 3.1.5 on 2021-01-27 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feescheduleitem',
            name='student_status',
        ),
        migrations.AddField(
            model_name='feeschedule',
            name='student_status',
            field=models.CharField(blank=True, choices=[('FD', 'Fresh Day'), ('FB', 'Fresh Boarder'), ('D', 'Day'), ('B', 'Boarder')], max_length=200, null=True),
        ),
    ]
