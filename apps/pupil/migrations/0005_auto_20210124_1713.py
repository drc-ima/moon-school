# Generated by Django 3.1.5 on 2021-01-24 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pupil', '0004_auto_20210122_1851'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pupil',
            name='guardian',
            field=models.CharField(blank=True, choices=[('P', 'Parent'), ('O', 'Other')], max_length=200, null=True),
        ),
    ]
