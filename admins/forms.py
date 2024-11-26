from django import forms
from .models import (
    Quiz, Question, MCQQuestion, ShortAnswerQuestion, 
    TrueFalseQuestion, MultiCorrectQuestion, FillInTheBlankQuestion, QuizUpload
)

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ('title', 'description', 'due_date')

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('text', 'question_type')

class MCQForm(forms.ModelForm):
    class Meta:
        model = MCQQuestion
        fields = ('choice1', 'choice2', 'choice3', 'choice4', 'correct_answer')

class MultiCorrectForm(forms.ModelForm):
    correct_answers = forms.MultipleChoiceField(
        choices=[
            ('choice1', 'Choice 1'), 
            ('choice2', 'Choice 2'), 
            ('choice3', 'Choice 3'), 
            ('choice4', 'Choice 4')
        ],
        widget=forms.CheckboxSelectMultiple,  # Render as checkboxes for multi-selection.
    )

    class Meta:
        model = MultiCorrectQuestion
        fields = ('choice1', 'choice2', 'choice3', 'choice4', 'correct_answers')

class ShortAnswerForm(forms.ModelForm):
    class Meta:
        model = ShortAnswerQuestion
        fields = ('correct_answer',)

class TrueFalseForm(forms.ModelForm):
    class Meta:
        model = TrueFalseQuestion
        fields = ('correct_answer',)

class FillInTheBlankForm(forms.ModelForm):
    correct_answers = forms.CharField(
        widget=forms.Textarea,  # Allow multiple answers in text area.
        help_text="Enter multiple correct answers separated by commas."
    )

    class Meta:
        model = FillInTheBlankQuestion
        fields = ('correct_answers',)

    def clean_correct_answers(self):
        """Convert the comma-separated input into a list of answers."""
        data = self.cleaned_data['correct_answers']
        answers = [answer.strip() for answer in data.split(',')]
        if not answers:
            raise forms.ValidationError("You must provide at least one correct answer.")
        return answers

class QuizUploadForm(forms.ModelForm):
    class Meta:
        model = QuizUpload
        fields = ['file', 'quiz_name', 'description', 'due_date']
