from django.contrib import admin
from . import models

@admin.register(models.Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code')
    search_fields = ('name', 'code')

@admin.register(models.Word)
class WordAdmin(admin.ModelAdmin):
    list_display = ('id', 'language', 'term', 'translation', 'part_of_speech')
    list_filter = ('language', 'part_of_speech')
    search_fields = ('term', 'translation')

@admin.register(models.Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('id', 'language', 'title')
    list_filter = ('language',)
    search_fields = ('title',)
    filter_horizontal = ('words',)

@admin.register(models.PracticeSession)
class PracticeSessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'language', 'lesson', 'question_count', 'correct_count', 'created_at')
    list_filter = ('language',)

@admin.register(models.PracticeQuestion)
class PracticeQuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'session', 'word', 'qtype', 'is_correct')
    list_filter = ('qtype', 'is_correct', 'session__language')
    search_fields = ('word__term', 'word__translation')
