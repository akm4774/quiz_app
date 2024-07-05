from django import forms
from students.models import Student
from admins.models import Quiz, Question
class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['enrollment', 'contact', 'city', 'state', 'gender', 'profile_picture']
        
