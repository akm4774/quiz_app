from django.urls import path, include
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.login_view, name='home'),
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),
    path('available-quizzes/', views.available_quizzes, name='available_quizzes'),
    path('take-quiz/<int:quiz_id>/', views.take_quiz, name='take_quiz'),
    path('quiz-history/', views.quiz_history, name='quiz_history'),
    path('profile/', views.student_profile, name='student_profile'),
    path('student_admin_dashboard/', views.student_admin_dashboard, name='student_admin_dashboard'),
]
