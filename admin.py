
from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from .models import Question, Choice, Submission
from .models import Lesson


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1


class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ('question_text', 'course')
    search_fields = ('question_text',)


class LessonAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]
    list_display = ('name', 'course')
    search_fields = ('name',)


admin.site.register(Question, QuestionAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Choice)
admin.site.register(Submission)
