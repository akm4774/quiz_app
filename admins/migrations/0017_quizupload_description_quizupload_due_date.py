# Generated by Django 5.0.1 on 2024-11-26 06:07

import admins.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admins', '0016_quizupload_quiz_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='quizupload',
            name='description',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='quizupload',
            name='due_date',
            field=models.DateTimeField(default=admins.models.one_day_from_now),
        ),
    ]