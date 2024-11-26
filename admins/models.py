from django.db import models
from django.utils import timezone
from datetime import timedelta

def one_day_from_now():
    return timezone.now() + timedelta(days=1)

class Quiz(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    due_date = models.DateTimeField(default=one_day_from_now)
    is_available_to_students = models.BooleanField(default=True)
    allowed_students = models.ManyToManyField('students.Student', blank=True)  # Allow selection of students
    max_attempts = models.PositiveIntegerField(default=1)  # Maximum allowed attempts
    duration = models.PositiveIntegerField(default=30)  # Duration in minutes

    def __str__(self):
        return self.title

class Question(models.Model):
    QUESTION_TYPES = [
        ('MCQ', 'Multiple Choice'),
        ('MULTI_CORRECT', 'Multi-Correct'),
        ('SHORT', 'Short Answer'),
        ('TRUE_FALSE', 'True/False'),
        ('FILL_BLANK', 'Fill-in-the-Blank'),
    ]

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.CharField(max_length=255)
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

class MCQQuestion(models.Model):
    question = models.OneToOneField(Question, on_delete=models.CASCADE)
    choice1 = models.CharField(max_length=255)
    choice2 = models.CharField(max_length=255)
    choice3 = models.CharField(max_length=255)
    choice4 = models.CharField(max_length=255)
    correct_answer = models.CharField(
        max_length=10,
        choices=[
            ('choice1', 'Choice 1'),
            ('choice2', 'Choice 2'),
            ('choice3', 'Choice 3'),
            ('choice4', 'Choice 4'),
        ]
    )

class MultiCorrectQuestion(models.Model):
    question = models.OneToOneField(Question, on_delete=models.CASCADE)
    choice1 = models.CharField(max_length=255)
    choice2 = models.CharField(max_length=255)
    choice3 = models.CharField(max_length=255)
    choice4 = models.CharField(max_length=255)
    correct_answers = models.JSONField()  # Store multiple correct answers as JSON.

    def save(self, *args, **kwargs):
        # Ensure correct answers are within valid choices
        valid_choices = {'choice1', 'choice2', 'choice3', 'choice4'}
        if not set(self.correct_answers).issubset(valid_choices):
            raise ValueError("Invalid correct answers")
        super().save(*args, **kwargs)

class ShortAnswerQuestion(models.Model):
    question = models.OneToOneField(Question, on_delete=models.CASCADE)
    correct_answer = models.CharField(max_length=255)

class TrueFalseQuestion(models.Model):
    question = models.OneToOneField(Question, on_delete=models.CASCADE)
    correct_answer = models.BooleanField()

class FillInTheBlankQuestion(models.Model):
    question = models.OneToOneField(Question, on_delete=models.CASCADE)
    correct_answers = models.JSONField()  # Store a list of acceptable answers.

    def save(self, *args, **kwargs):
        if not isinstance(self.correct_answers, list):
            raise ValueError("Correct answers must be a list")
        super().save(*args, **kwargs)

class QuizUpload(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    quiz_name = models.CharField(max_length=255, default="default_quiz_name")
    description = models.TextField(default="")  # Add description for the quiz
    due_date = models.DateTimeField(default=one_day_from_now)  # Optional field for the quiz due date
