# Generated by Django 5.0.1 on 2024-10-24 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admins', '0013_remove_question_choice1_remove_question_choice2_and_more'),
        ('students', '0005_quizresult_attempt_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='allowed_students',
            field=models.ManyToManyField(blank=True, to='students.student'),
        ),
        migrations.AddField(
            model_name='quiz',
            name='duration',
            field=models.PositiveIntegerField(default=30),
        ),
        migrations.AddField(
            model_name='quiz',
            name='max_attempts',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
