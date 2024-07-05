from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('create-quiz/', views.create_quiz, name='create_quiz'),
    path('create-question/', views.create_question, name='create_question'),
    path('edit-quiz/<int:quiz_id>/', views.edit_quiz, name='edit_quiz'),
    path('create-choice/', views.create_choice, name='create_choice'),
    path('delete-quiz/<int:quiz_id>/', views.delete_quiz, name='delete_quiz'),
    path('logout/', auth_views.LogoutView.as_view(template_name='students/registration/logout.html'), name='logout'),
]
