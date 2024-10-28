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
            quiz = form.save()
            # Set the selected students for this quiz
            selected_students = request.POST.getlist('students')
            quiz.allowed_students.set(selected_students)
            return redirect('create_question', quiz_id=quiz.id)
    else:
        form = QuizForm()

    students = Student.objects.all()  # Fetch all students for the selection
    return render(request, 'admins/create_quiz.html', {'form': form, 'students': students})


@login_required
def create_question(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)

    if request.method == 'POST':
        form = QuestionForm(request.POST)  # Generic question form
        if form.is_valid():
            question = form.save(commit=False)
            question.quiz = quiz  # Associate the new question with the quiz
            question.save()
            # Redirect to create_specific_question view for further details
            return redirect('create_specific_question', question_id=question.id)

    else:
        form = QuestionForm()

    return render(request, 'admins/create_question.html', {'form': form, 'quiz': quiz})

@login_required
def create_specific_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)

    # Determine the specific model class and form based on question type
    specific_question_model = None
    form_class = None

    if question.question_type == 'MCQ':
        specific_question_model = MCQQuestion
        form_class = MCQForm
    elif question.question_type == 'MULTI_CORRECT':
        specific_question_model = MultiCorrectQuestion
        form_class = MultiCorrectForm
    elif question.question_type == 'SHORT':
        specific_question_model = ShortAnswerQuestion
        form_class = ShortAnswerForm
    elif question.question_type == 'TRUE_FALSE':
        specific_question_model = TrueFalseQuestion
        form_class = TrueFalseForm
    elif question.question_type == 'FILL_BLANK':
        specific_question_model = FillInTheBlankQuestion
        form_class = FillInTheBlankForm

    # Check if a specific question already exists for this question
    specific_question = None
    if specific_question_model:
        specific_question = specific_question_model.objects.filter(question=question).first()

    if request.method == 'POST':
        # Use the existing specific question instance or create a new one if it doesn't exist
        form = form_class(request.POST, instance=specific_question)
        if form.is_valid():
            specific_instance = form.save(commit=False)
            specific_instance.question = question  # Associate with the parent question
            specific_instance.save()
            return redirect('edit_quiz', pk=question.quiz.id)
    else:
        form = form_class(instance=specific_question)

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
            return redirect('admin_dashboard')
    else:
        form = QuizForm(instance=quiz)

    students = Student.objects.all()
    questions = quiz.questions.all()

    return render(request, 'admins/edit_quiz.html', {
        'form': form,
        'quiz': quiz,
        'questions': questions,
        'students': students
    })
@login_required
def edit_question(request, quiz_pk, question_pk):
    quiz = get_object_or_404(Quiz, pk=quiz_pk)
    question = get_object_or_404(Question, pk=question_pk, quiz=quiz)

    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save()
            # Redirect to edit the specific question type details
            return redirect('create_specific_question', question_id=question.pk)
    else:
        form = QuestionForm(instance=question)

    return render(request, 'admins/edit_question.html', {
        'form': form,
        'quiz': quiz,
        'question': question,
    })


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