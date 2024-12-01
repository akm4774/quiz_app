from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.urls import reverse_lazy
from students.models import Student, QuizResult, StudentAnswer, CodingSubmission
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
from admins.models import Quiz, Question, CodingQuestion
from django.db.models import Avg, Count, Max
from collections import defaultdict
import io
import sys
@login_required
def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    student = request.user.student

    # Check if the student is allowed to take the quiz
    if student not in quiz.allowed_students.all():
        return render(request, 'students/quiz_access_denied.html')

    # Check attempt limits
    attempts = QuizResult.objects.filter(student=student, quiz=quiz).count()
    if attempts >= quiz.max_attempts:
        return render(request, 'students/max_attempts_reached.html')
    
    if 'quiz_start_time' not in request.session:
        request.session['quiz_start_time'] = str(timezone.now())

    start_time = timezone.datetime.fromisoformat(request.session['quiz_start_time'])
    elapsed_time = (timezone.now() - start_time).seconds / 60  # in minutes

    if elapsed_time > quiz.duration:
        return render(request, 'students/quiz_time_exceeded.html')

    questions = quiz.questions.all()
    non_coding_questions = questions.exclude(question_type='CODING')
    coding_questions = questions.filter(question_type='CODING')
    if coding_questions.exists():
        return redirect('submit_coding_question', question_id=coding_questions.first().id)

    if request.method == 'POST':
        score = 0

        # Process non-coding questions
        for question in non_coding_questions:
            user_answer = request.POST.get(f'question_{question.id}')
            correct_answer = None

            if question.question_type == 'MCQ':
                correct_answer = question.mcqquestion.correct_answer
            elif question.question_type == 'TRUE_FALSE':
                correct_answer = str(question.truefalsequestion.correct_answer)
            elif question.question_type == 'SHORT':
                correct_answer = question.shortanswerquestion.correct_answer
            elif question.question_type == 'FILL_BLANK':
                correct_answers = question.fillintheblankquestion.correct_answers
                is_correct = user_answer in correct_answers
            elif question.question_type == 'MULTI_CORRECT':
                correct_answers = question.multicorrectquestion.correct_answers
                user_answers = request.POST.getlist(f'question_{question.id}')
                is_correct = set(user_answers) == set(correct_answers)

            if correct_answer is not None:
                is_correct = user_answer == correct_answer

            StudentAnswer.objects.create(
                student=student,
                question=question,
                answer=user_answer,
                is_correct=is_correct
            )

            if is_correct:
                score += 1

        # Save quiz progress excluding coding questions
        score_percentage = (score / non_coding_questions.count()) * 100 if non_coding_questions.exists() else 0.00

        QuizResult.objects.create(
            student=student,
            quiz=quiz,
            score=score_percentage,
            taken_at=timezone.now(),
            attempt_number=attempts + 1
        )

        return redirect('quiz_history')

    return render(request, 'students/take_quiz.html', {
        'quiz': quiz,
        'non_coding_questions': non_coding_questions,
        'coding_questions': coding_questions
    })

@login_required
def quiz_history(request):
    student = request.user.student
    quiz_results = QuizResult.objects.filter(student=student).order_by('-taken_at')
    
    return render(request, 'students/quiz_history.html', {
        'quiz_results': quiz_results
    })
@login_required
def quiz_review(request, quiz_result_id):
    quiz_result = get_object_or_404(QuizResult, id=quiz_result_id)
    student = quiz_result.student

    student_answers = StudentAnswer.objects.filter(student=student, question__quiz=quiz_result.quiz)

    coding_submissions = CodingSubmission.objects.filter(
        student=student, question__quiz=quiz_result.quiz
    )

    # Map coding submissions by question ID
    coding_answers = {submission.question.id: submission for submission in coding_submissions}

    return render(request, 'students/quiz_review.html', {
        'quiz_result': quiz_result,
        'student_answers': student_answers,
        'coding_answers': coding_answers,
    })

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
    quizzes = Quiz.objects.all()  # Filter quizzes if needed
    return render(request, 'students/student_dashboard.html', {'quizzes': quizzes})

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


@login_required
def quiz_ranking(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    results = QuizResult.objects.filter(quiz=quiz).order_by('-score')

    # Calculate rank of the current student
    student_result = results.filter(student=request.user.student).first()
    rank = list(results).index(student_result) + 1 if student_result else None

    # Calculate stats
    max_score = results.aggregate(Max('score'))['score__max']
    avg_score = results.aggregate(Avg('score'))['score__avg']

    return render(request, 'students/quiz_ranking.html', {
        'quiz': quiz,
        'results': results,
        'rank': rank,
        'max_score': max_score,
        'avg_score': avg_score
    })
@login_required
def submit_coding_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    coding_question = get_object_or_404(CodingQuestion, question=question)
    student = request.user.student

    submitted_code = request.POST.get('submitted_code', '')

    # Default variable values
    test_case_1_result = request.POST.get('test_case_1_result') == 'True'
    test_case_2_result = request.POST.get('test_case_2_result') == 'True'
    is_correct = request.POST.get('is_correct') == 'True'
    feedback = request.POST.get('feedback', '')

    def execute_code_with_input(code, input_string):
        try:
            input_lines = iter(input_string.splitlines())
            global_scope = {"input": lambda: next(input_lines)}

            output_capture = io.StringIO()
            sys.stdout = output_capture
            exec(code, global_scope)
            sys.stdout = sys.__stdout__

            return output_capture.getvalue().strip(), None
        except Exception as e:
            sys.stdout = sys.__stdout__
            return None, str(e)

    if request.method == 'POST':
        if 'run_code' in request.POST:
            # Run test cases
            output1, error1 = execute_code_with_input(submitted_code, coding_question.test_case_1_input)
            test_case_1_result = output1 == coding_question.test_case_1_output

            output2, error2 = execute_code_with_input(submitted_code, coding_question.test_case_2_input)
            test_case_2_result = output2 == coding_question.test_case_2_output

            is_correct = test_case_1_result and test_case_2_result
            feedback = "All test cases passed!" if is_correct else "One or more test cases failed."

            if error1 or error2:
                feedback += f"\nError: {error1 or error2}"

            return render(request, 'students/submit_coding_question.html', {
                'question': question,
                'submitted_code': submitted_code,
                'test_case_1_result': test_case_1_result,
                'test_case_2_result': test_case_2_result,
                'submitted_output_1': output1,
                'submitted_output_2': output2,
                'is_correct': is_correct,
                'feedback': feedback,
                'test_case_1_output': coding_question.test_case_1_output,
                'test_case_2_output': coding_question.test_case_2_output,
            })

        elif 'submit_code' in request.POST:
            # Save the submission
            coding_submission = CodingSubmission.objects.create(
                student=student,
                question=question,
                submitted_code=submitted_code,
                is_correct=is_correct,
                test_case_1_result=test_case_1_result,
                test_case_2_result=test_case_2_result,
                feedback=feedback,
            )

            # Save student answer
            student_answer = StudentAnswer.objects.create(
                student=student,
                question=question,
                answer=submitted_code,
                is_correct=is_correct,
            )
            print(f"StudentAnswer created: {student_answer}")
            # Recalculate quiz score if needed
            quiz = question.quiz
            student_answers = StudentAnswer.objects.filter(student=student, question__quiz=quiz)

            # Calculate the quiz score
            score = sum(1 for answer in student_answers if answer.is_correct)
            score_percentage = (score / quiz.questions.count()) * 100 if quiz.questions.exists() else 0.00

            quiz_result, created = QuizResult.objects.update_or_create(
                student=student, quiz=quiz,
                defaults={
                    'score': score_percentage,
                    'taken_at': timezone.now(),
                }
            )

            print(f"Redirecting to review page for QuizResult ID: {quiz_result.id}")
            return redirect('quiz_review', quiz_result_id=quiz_result.id)


    return render(request, 'students/submit_coding_question.html', {
        'question': question,
        'submitted_code': submitted_code,
        'test_case_1_result': test_case_1_result,
        'test_case_2_result': test_case_2_result,
        'is_correct': is_correct,
        'feedback': feedback,
    })
