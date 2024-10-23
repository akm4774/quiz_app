from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import (
    QuizForm, QuestionForm, MCQForm, ShortAnswerForm, 
    TrueFalseForm, MultiCorrectForm, FillInTheBlankForm
)
from .models import (
    Quiz, Question, MCQQuestion, ShortAnswerQuestion, 
    TrueFalseQuestion, MultiCorrectQuestion, FillInTheBlankQuestion
)

@login_required
def admin_dashboard(request):
    quizzes = Quiz.objects.all()
    return render(request, 'admins/admin_dashboard.html', {'quizzes': quizzes})

@login_required
def create_quiz(request):
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save()  # Save the quiz and store the instance
            return redirect('create_question', quiz_id=quiz.id)  # Redirect to add questions
    else:
        form = QuizForm()
    return render(request, 'admins/create_quiz.html', {'form': form})



@login_required
def create_question(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.quiz = quiz
            question.save()
            return redirect('create_specific_question', question_id=question.id)
        else:
            print(form.errors)  # Debugging: Print form errors to console

    else:
        form = QuestionForm()
    
    return render(request, 'admins/create_question.html', {'form': form, 'quiz': quiz})
@login_required
def create_specific_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    
    # Determine which form to show based on question type
    form_class = None
    if question.question_type == 'MCQ':
        form_class = MCQForm
    elif question.question_type == 'MULTI_CORRECT':
        form_class = MultiCorrectForm
    elif question.question_type == 'SHORT':
        form_class = ShortAnswerForm
    elif question.question_type == 'TRUE_FALSE':
        form_class = TrueFalseForm
    elif question.question_type == 'FILL_BLANK':
        form_class = FillInTheBlankForm

    if request.method == 'POST':
        if form_class:
            form = form_class(request.POST)
            if form.is_valid():
                # Save the specific question model (MCQ, MultiCorrect, etc.)
                specific_question = form.save(commit=False)
                specific_question.question = question
                specific_question.save()
                print(f'Successfully saved: {specific_question}')  # Debugging: Confirm save
                return redirect('edit_quiz', pk=question.quiz.id)
            else:
                print("Form is not valid:", form.errors)  # Debugging: Show form errors in console
        else:
            print("No form class found for the question type.")
            return redirect('edit_quiz', pk=question.quiz.id)

    else:
        form = form_class() if form_class else None

    return render(request, 'admins/create_specific_question.html', {
        'form': form,
        'question': question,
    })
def edit_quiz(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    if request.method == 'POST':
        form = QuizForm(request.POST, instance=quiz)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = QuizForm(instance=quiz)
    return render(request, 'admins/edit_quiz.html', {'form': form, 'quiz': quiz})

def edit_question(request, quiz_pk, question_pk):
    question = get_object_or_404(Question, pk=question_pk)

    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            return redirect('edit_quiz', pk=quiz_pk)
    else:
        form = QuestionForm(instance=question)

    context = {'quiz_pk': quiz_pk, 'form': form}
    return render(request, 'admins/edit_question.html', context)

def delete_question(request, pk):
    question = get_object_or_404(Question, pk=pk)
    quiz_id = question.quiz.pk
    question.delete()
    return redirect('edit_quiz', pk=quiz_id)

def delete_quiz(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    quiz.delete()
    return redirect('admin_dashboard')
