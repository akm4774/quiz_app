# admins/forms.py
from django import forms
from admins.models import Quiz, Question, Choice
from students.models import Student  # Import the Student model

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'description', 'due_date', 'assigned_students']
        widgets = {
            'assigned_students': forms.CheckboxSelectMultiple(),
        }

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['quiz', 'question_text']

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['question', 'text', 'is_correct']
