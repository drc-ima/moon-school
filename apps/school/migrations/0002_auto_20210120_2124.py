# Generated by Django 3.1.5 on 2021-01-20 21:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='school',
            name='logo',
            field=models.FileField(blank=True, null=True, upload_to='school/'),
        ),
    ]
