from django.contrib import admin
from .models import Quiz, Question

class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'due_date', 'is_available_to_students', 'max_attempts')
    filter_horizontal = ('allowed_students',)  # For easy selection of students

admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question)
