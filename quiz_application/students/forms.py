from django import forms
from .models import Student, Quiz, Question
class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['enrollment', 'contact', 'city', 'state', 'gender', 'profile_picture']
        
class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'description', 'schedule']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text', 'option_1', 'option_2', 'option_3', 'option_4', 'correct_option']