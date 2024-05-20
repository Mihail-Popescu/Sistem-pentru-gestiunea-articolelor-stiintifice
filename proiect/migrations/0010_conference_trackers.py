# Generated by Django 4.1.13 on 2024-05-20 00:43

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proiect', '0009_rename_date_conference_end_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='conference',
            name='trackers',
            field=models.ManyToManyField(blank=True, related_name='tracked_conferences', to=settings.AUTH_USER_MODEL),
        ),
    ]