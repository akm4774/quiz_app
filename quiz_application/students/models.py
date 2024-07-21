from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from admins.models import Quiz
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    enrollment = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    gender = models.CharField(max_length=10)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return self.user.username

class Profile(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    academic_records = models.TextField()

    def __str__(self):
        return self.student.user.username

@receiver(post_save, sender=Student)
def create_or_update_student_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(student=instance)
    instance.profile.save()

class QuizResult(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=5, decimal_places=2)
    taken_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.student.user.username} - {self.quiz.title}'
