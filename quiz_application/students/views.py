from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.urls import reverse_lazy
from .models import Student
from .forms import StudentProfileForm
from django.contrib.auth.decorators import login_required

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Student.objects.create(user=user)  # Create a student profile
            login(request, user)
            return redirect('student_dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('student_dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

@login_required
def student_dashboard(request):
    return render(request, 'students/student_dashboard.html')

@login_required
def available_quizzes(request):
    # Fetch and display available quizzes
    return render(request, 'students/available_quizzes.html')

@login_required
def take_quiz(request, quiz_id):
    # Handle quiz taking logic
    return render(request, 'students/take_quiz.html')

@login_required
def quiz_history(request):
    # Display quiz history for the student
    return render(request, 'students/quiz_history.html')

@login_required
def student_profile(request):
    student = request.user.student
    if request.method == 'POST':
        form = StudentProfileForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student_profile')
    else:
        form = StudentProfileForm(instance=student)
    return render(request, 'students/student_profile.html', {'form': form})
