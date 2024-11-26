from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import (
    QuizForm, QuestionForm, MCQForm, ShortAnswerForm, 
    TrueFalseForm, MultiCorrectForm, FillInTheBlankForm, QuizUploadForm
)
from .models import (
    Quiz, Question, MCQQuestion, ShortAnswerQuestion, 
    TrueFalseQuestion, MultiCorrectQuestion, FillInTheBlankQuestion
)
from students.models import QuizResult, Student
import csv
import logging
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




logger = logging.getLogger(__name__)

def upload_quiz(request):
    if request.method == 'POST':  # When user submits the form
        form = QuizUploadForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                # Retrieve the form data
                file = request.FILES['file']
                quiz_name = form.cleaned_data.get('quiz_name')
                description = form.cleaned_data.get('description')
                due_date = form.cleaned_data.get('due_date')

                # Create a new quiz
                quiz = Quiz.objects.create(
                    title=quiz_name,
                    description=description,
                    due_date=due_date,
                    is_available_to_students=True,  # Default value
                    max_attempts=1,  # Default value
                    duration=30  # Default value
                )

                # Process the uploaded CSV file
                decoded_file = file.read().decode('utf-8').splitlines()
                reader = csv.reader(decoded_file)

                # Iterate through each row in the CSV
                for index, row in enumerate(reader):
                    # Skip the header row
                    if index == 0:
                        continue

                    # Ensure the row has the correct number of fields
                    if len(row) != 6:
                        raise ValueError(f"Row {index + 1} does not have 6 columns.")

                    # Extract data from the row
                    question_text, choice1, choice2, choice3, choice4, correct_answer = row

                    # Validate the correct answer
                    valid_answers = {'choice1', 'choice2', 'choice3', 'choice4'}
                    if correct_answer not in valid_answers:
                        raise ValueError(f"Row {index + 1}: Invalid correct answer '{correct_answer}'.")

                    # Create the Question and MCQQuestion
                    question = Question.objects.create(
                        quiz=quiz,
                        text=question_text,
                        question_type='MCQ',  # Ensure it's an MCQ question
                    )
                    MCQQuestion.objects.create(
                        question=question,
                        choice1=choice1,
                        choice2=choice2,
                        choice3=choice3,
                        choice4=choice4,
                        correct_answer=correct_answer,
                    )

                return redirect('admin_dashboard')  # Redirect to the quiz list view

            except Exception as e:
                logger.error(f"Error processing the file: {e}")
                return render(request, 'admins/upload_quiz.html', {
                    'form': form,
                    'error': f"An error occurred while processing the file: {str(e)}",
                })
    else:  # For GET requests, display the form
        form = QuizUploadForm()

    return render(request, 'admins/upload_quiz.html', {'form': form})
