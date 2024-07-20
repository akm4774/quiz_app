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

from django.db import models

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    choice1 = models.CharField(max_length=255)
    choice2 = models.CharField(max_length=255)
    choice3 = models.CharField(max_length=255)
    choice4 = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=255)