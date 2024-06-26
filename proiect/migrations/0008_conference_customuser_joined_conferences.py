# Generated by Django 4.1.13 on 2024-05-19 23:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('proiect', '0007_customuser_is_organizer_customuser_is_tracker'),
    ]

    operations = [
        migrations.CreateModel(
            name='Conference',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('date', models.DateField()),
                ('location', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('picture', models.ImageField(blank=True, null=True, upload_to='conference_pictures/')),
                ('organizer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='organized_conferences', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='customuser',
            name='joined_conferences',
            field=models.ManyToManyField(blank=True, related_name='participants', to='proiect.conference'),
        ),
    ]
