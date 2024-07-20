from django import forms
from .models import Quiz, Question

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ('title', 'description')

class QuestionForm(forms.ModelForm):
    correct_answer = forms.CharField(label='Correct Answer', widget=forms.RadioSelect(choices=[
        ('choice1', 'Choice 1'),
        ('choice2', 'Choice 2'),
        ('choice3', 'Choice 3'),
        ('choice4', 'Choice 4'),
    ]))

    class Meta:
        model = Question
        fields = ('text', 'choice1', 'choice2', 'choice3', 'choice4', 'correct_answer')