from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.urls import reverse_lazy
from students.models import Student, QuizResult, StudentAnswer
from .forms import StudentProfileForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from admins.models import Quiz
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from admins.views import admin_dashboard
from admins.models import Quiz, Question

@login_required
def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()

    if request.method == 'POST':
        student = request.user.student
        score = 0

        for question in questions:
            user_answer = request.POST.get(f'question_{question.id}')
            correct_answer = None

            # Retrieve the correct answer based on the question type
            if question.question_type == 'MCQ':
                correct_answer = question.mcqquestion.correct_answer
            elif question.question_type == 'TRUE_FALSE':
                correct_answer = str(question.truefalsequestion.correct_answer)  # Boolean to string
            elif question.question_type == 'SHORT':
                correct_answer = question.shortanswerquestion.correct_answer
            elif question.question_type == 'FILL_BLANK':
                correct_answers = question.fillintheblankquestion.correct_answers
                is_correct = user_answer in correct_answers  # Check if answer is among the accepted ones
            elif question.question_type == 'MULTI_CORRECT':
                correct_answers = question.multicorrectquestion.correct_answers
                user_answers = request.POST.getlist(f'question_{question.id}')  # For multiple answers
                is_correct = set(user_answers) == set(correct_answers)  # Check if sets match

            # For non-FILL_BLANK and non-MULTI_CORRECT questions, compare directly
            if correct_answer is not None:
                is_correct = user_answer == correct_answer

            # Save the student's answer
            StudentAnswer.objects.create(
                student=student,
                question=question,
                answer=user_answer,
                is_correct=is_correct
            )

            # Increment the score if the answer is correct
            if is_correct:
                score += 1

        # Calculate score percentage
        score_percentage = (score / questions.count()) * 100

        # Save the quiz result
        QuizResult.objects.create(
            student=student,
            quiz=quiz,
            score=score_percentage,
            taken_at=timezone.now()
        )

        return redirect('quiz_history')

    return render(request, 'students/take_quiz.html', {'quiz': quiz, 'questions': questions})

@login_required
def quiz_history(request):
    student = request.user.student
    quiz_results = QuizResult.objects.filter(student=student)
    return render(request, 'students/quiz_history.html', {'quiz_results': quiz_results})

@login_required
def review_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    student = request.user.student
    answers = StudentAnswer.objects.filter(student=student, question__quiz=quiz)

    return render(request, 'students/review_quiz.html', {'quiz': quiz, 'answers': answers})

@login_required
def available_quizzes(request):
    student = request.user.student
    quizzes = Quiz.objects.filter(due_date__gt=timezone.now(), is_available_to_students=True)
    return render(request, 'students/available_quizzes.html', {'quizzes': quizzes})
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

def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('student_admin_dashboard')
        return redirect('student_dashboard')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            if user.is_superuser:
                return redirect('student_admin_dashboard')
            return redirect('student_dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

@login_required
def student_dashboard(request):
    return render(request, 'students/student_dashboard.html')

def student_admin_dashboard(request):
    return admin_dashboard(request)




@login_required
def student_profile(request):
    student = request.user.student
    if request.method == 'POST':
        profile_form = StudentProfileForm(request.POST, request.FILES, instance=student)
        password_form = PasswordChangeForm(request.user, request.POST)
        if profile_form.is_valid() and password_form.is_valid():
            profile_form.save()
            user = password_form.save()
            update_session_auth_hash(request, user)  # Important to keep the user logged in
            return redirect('student_profile')
    else:
        profile_form = StudentProfileForm(instance=student)
        password_form = PasswordChangeForm(request.user)
    return render(request, 'students/student_profile.html', {
        'profile_form': profile_form,
        'password_form': password_form,
        'username': request.user.username
    })

@login_required
def logout_view(request):
    logout(request)
    return render(request, 'registration/logout.html')
