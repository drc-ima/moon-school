# Generated by Django 3.1.5 on 2021-01-30 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0003_auto_20210128_1442'),
    ]

    operations = [
        migrations.AddField(
            model_name='receipt',
            name='last_printed',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='receipt',
            name='status',
            field=models.IntegerField(blank=True, choices=[(1, 'Full Payment'), (0, 'Part Payment')], null=True),
        ),
        migrations.AddField(
            model_name='receipt',
            name='words',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='feeschedule',
            name='student_status',
            field=models.CharField(blank=True, choices=[('FB', 'Fresh Boarder'), ('B', 'Boarders'), ('FD', 'Fresh Day'), ('D', 'Days')], max_length=200, null=True),
        ),
    ]
