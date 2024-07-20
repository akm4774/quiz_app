from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import QuizForm, QuestionForm
from .models import Quiz, Question

@login_required
def admin_dashboard(request):
    quizzes = Quiz.objects.all()
    return render(request, 'admins/admin_dashboard.html', {'quizzes': quizzes})

@login_required
def create_quiz(request):
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = QuizForm()
    return render(request, 'admins/create_quiz.html', {'form': form})

@login_required
def create_question(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.quiz = quiz
            question.save()
            return redirect('admin_dashboard')
    else:
        form = QuestionForm()
    return render(request, 'admins/create_question.html', {'form': form, 'quiz': quiz})

def edit_quiz(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    if request.method == 'POST':
        form = QuizForm(request.POST, instance=quiz)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')  # redirect to admin dashboard view
    else:
        form = QuizForm(instance=quiz)
    return render(request, 'admins/edit_quiz.html', {'form': form, 'quiz': quiz})

def delete_question(request, pk):
    question = Question.objects.get(pk=pk)
    question.delete()
    return redirect('edit_quiz', pk=question.quiz.pk)

def delete_quiz(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    quiz.delete()
    return redirect('admin_dashboard')

def edit_question(request, quiz_pk, question_pk):
    # ... get the question object using quiz_pk and question_pk
    question = Question.objects.get(pk=question_pk)

    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            return redirect('edit_quiz', pk=quiz_pk)  # Redirect back to the quiz edit view
    else:
        form = QuestionForm(instance=question)

    context = {
        'quiz_pk': quiz_pk,
        'form': form,
    }
    return render(request, 'admins/edit_question.html', context)