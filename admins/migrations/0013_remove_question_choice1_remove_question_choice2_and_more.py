# Generated by Django 5.0.1 on 2024-10-22 10:17

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admins', '0012_alter_question_correct_answer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='choice1',
        ),
        migrations.RemoveField(
            model_name='question',
            name='choice2',
        ),
        migrations.RemoveField(
            model_name='question',
            name='choice3',
        ),
        migrations.RemoveField(
            model_name='question',
            name='choice4',
        ),
        migrations.RemoveField(
            model_name='question',
            name='correct_answer',
        ),
        migrations.AddField(
            model_name='question',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='question',
            name='question_type',
            field=models.CharField(choices=[('MCQ', 'Multiple Choice'), ('MULTI_CORRECT', 'Multi-Correct'), ('SHORT', 'Short Answer'), ('TRUE_FALSE', 'True/False'), ('FILL_BLANK', 'Fill-in-the-Blank')], default='MCQ', max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='question',
            name='quiz',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='admins.quiz'),
        ),
        migrations.CreateModel(
            name='FillInTheBlankQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('correct_answers', models.JSONField()),
                ('question', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='admins.question')),
            ],
        ),
        migrations.CreateModel(
            name='MCQQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice1', models.CharField(max_length=255)),
                ('choice2', models.CharField(max_length=255)),
                ('choice3', models.CharField(max_length=255)),
                ('choice4', models.CharField(max_length=255)),
                ('correct_answer', models.CharField(choices=[('choice1', 'Choice 1'), ('choice2', 'Choice 2'), ('choice3', 'Choice 3'), ('choice4', 'Choice 4')], max_length=10)),
                ('question', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='admins.question')),
            ],
        ),
        migrations.CreateModel(
            name='MultiCorrectQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice1', models.CharField(max_length=255)),
                ('choice2', models.CharField(max_length=255)),
                ('choice3', models.CharField(max_length=255)),
                ('choice4', models.CharField(max_length=255)),
                ('correct_answers', models.JSONField()),
                ('question', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='admins.question')),
            ],
        ),
        migrations.CreateModel(
            name='ShortAnswerQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('correct_answer', models.CharField(max_length=255)),
                ('question', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='admins.question')),
            ],
        ),
        migrations.CreateModel(
            name='TrueFalseQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('correct_answer', models.BooleanField()),
                ('question', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='admins.question')),
            ],
        ),
    ]
