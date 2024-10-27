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
from students.models import QuizResult, Student

@login_required
def admin_dashboard(request):
    quizzes = Quiz.objects.all()
    return render(request, 'admins/admin_dashboard.html', {'quizzes': quizzes})

@login_required
def create_quiz(request):
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save()  # Save the quiz and get the instance
            return redirect('create_question', quiz_id=quiz.id)  # Redirect to add questions for the quiz
    else:
        form = QuizForm()

    return render(request, 'admins/create_quiz.html', {'form': form})


@login_required
def create_question(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)

    if request.method == 'POST':
        form = QuestionForm(request.POST)  # Assume you have a form for questions
        if form.is_valid():
            question = form.save(commit=False)
            question.quiz = quiz  # Associate the new question with the quiz
            question.save()
            return redirect('edit_quiz', pk=quiz_id)  # Redirect to quiz edit page

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
@login_required
def edit_quiz(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)

    if request.method == 'POST':
        form = QuizForm(request.POST, instance=quiz)
        if form.is_valid():
            quiz = form.save()
            # Update allowed students for the quiz
            selected_students = request.POST.getlist('students')
            quiz.allowed_students.set(selected_students)
            quiz.save()
            return redirect('admin_dashboard')
    else:
        form = QuizForm(instance=quiz)

    # Get all students for selection in the form
    students = Student.objects.all()
    questions = quiz.questions.all()
    
    return render(request, 'admins/edit_quiz.html', {
        'form': form,
        'quiz': quiz,
        'questions': questions,
        'students': students
    })
@login_required
def edit_question(request, quiz_id, question_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    question = get_object_or_404(Question, pk=question_id)

    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            return redirect('edit_quiz', pk=quiz_id)  # Redirect back to quiz edit page

    else:
        form = QuestionForm(instance=question)

    return render(request, 'admins/edit_question.html', {'form': form, 'quiz': quiz, 'question': question})


@login_required
def delete_question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    quiz_id = question.quiz.id  # Get the associated quiz ID before deleting
    question.delete()
    return redirect('edit_quiz', pk=quiz_id)  # Redirect to the quiz edit page


def delete_quiz(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    quiz.delete()
    return redirect('admin_dashboard')

def quiz_performance(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    results = QuizResult.objects.filter(quiz=quiz).order_by('-taken_at')
    
    student_data = {}
    for result in results:
        if result.student not in student_data:
            student_data[result.student] = {
                'attempts': 0,
                'scores': []
            }
        student_data[result.student]['attempts'] += 1
        student_data[result.student]['scores'].append(result.score)
    
    return render(request, 'admins/quiz_performance.html', {
        'quiz': quiz,
        'student_data': student_data
    })