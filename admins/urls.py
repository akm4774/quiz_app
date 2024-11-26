from django.urls import path
from . import views

urlpatterns = [
    # Admin Dashboard
    path('', views.admin_dashboard, name='admin_dashboard'),  # Admin home/dashboard

    # Quiz Management
    path('create-quiz/', views.create_quiz, name='create_quiz'),  # Create a new quiz
    path('quiz/<int:pk>/edit/', views.edit_quiz, name='edit_quiz'),  # Edit a quiz
    path('quiz/<int:pk>/delete/', views.delete_quiz, name='delete_quiz'),  # Delete a quiz

    # Question Management
    path('quiz/<int:quiz_id>/create-question/', views.create_question, name='create_question'),  # Create a question for a quiz
    path('quiz/<int:quiz_pk>/question/<int:question_pk>/edit/', views.edit_question, name='edit_question'),  # Edit an existing question
    path('question/<int:question_id>/delete/', views.delete_question, name='delete_question'),  # Delete a question

    # Create Specific Question Type (e.g., MCQ, True/False, etc.)
    path('question/<int:question_id>/create-specific/', views.create_specific_question, name='create_specific_question'),

    # Quiz Performance View
    path('quiz/<int:quiz_id>/performance/', views.quiz_performance, name='quiz_performance'),  # Performance analysis
    path('upload-quiz/', views.upload_quiz, name='upload_quiz'),
]
