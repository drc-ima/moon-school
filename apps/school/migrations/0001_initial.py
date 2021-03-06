# Generated by Django 3.1.5 on 2021-01-20 00:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('school_id', models.CharField(blank=True, max_length=200, null=True)),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('slug', models.SlugField(blank=True, null=True, unique=True)),
                ('uuid', models.UUIDField(blank=True, default=uuid.uuid4, null=True, unique=True)),
                ('logo', models.URLField(blank=True, max_length=3000, null=True)),
                ('domain', models.CharField(blank=True, max_length=200, null=True)),
                ('gps_address', models.CharField(blank=True, max_length=200, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=200, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='institutions', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'school',
            },
        ),
    ]
