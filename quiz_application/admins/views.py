# admins/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from .forms import QuizForm, QuestionForm, ChoiceForm
from .models import Quiz, Question, Choice
from django.forms import modelformset_factory
from django.contrib.auth import logout
def is_admin(user):
    return user.is_superuser

@user_passes_test(is_admin)
def admin_dashboard(request):
    quizzes = Quiz.objects.all()
    return render(request, 'admins/admin_dashboard.html', {'quizzes': quizzes})

@user_passes_test(is_admin)
def create_quiz(request):
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = QuizForm()
    return render(request, 'admins/create_quiz.html', {'form': form})

@user_passes_test(is_admin)
def edit_quiz(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    if request.method == 'POST':
        form = QuizForm(request.POST, instance=quiz)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = QuizForm(instance=quiz)
    return render(request, 'admins/edit_quiz.html', {'form': form})

@user_passes_test(is_admin)
def create_question(request):
    ChoiceFormSet = modelformset_factory(Choice, form=ChoiceForm, extra=4)
    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        choice_formset = ChoiceFormSet(request.POST)
        if question_form.is_valid() and choice_formset.is_valid():
            question = question_form.save()
            choices = choice_formset.save(commit=False)
            for choice in choices:
                choice.question = question
                choice.save()
            return redirect('admin_dashboard')
    else:
        question_form = QuestionForm()
        choice_formset = ChoiceFormSet(queryset=Choice.objects.none())
    return render(request, 'admins/create_question.html', {
        'question_form': question_form,
        'choice_formset': choice_formset
    })

@user_passes_test(is_admin)
def create_choice(request):
    if request.method == 'POST':
        form = ChoiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = ChoiceForm()
    return render(request, 'admins/create_choice.html', {'form': form})
@user_passes_test(is_admin)
def delete_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    quiz.delete()
    messages.success(request, 'Quiz deleted successfully')
    return redirect('admin_dashboard')

@user_passes_test(is_admin)
def logout_view(request):
    logout(request)
    return render(request, 'registration/logout.html')