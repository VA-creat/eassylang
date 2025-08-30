from django.db import models
from django.utils import timezone
import uuid

class Language(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return f"{self.name} ({self.code})"

class Word(models.Model):
    POS_CHOICES = [
        ('noun', 'Noun'),
        ('verb', 'Verb'),
        ('adj', 'Adjective'),
        ('adv', 'Adverb'),
        ('phrase', 'Phrase'),
        ('other', 'Other'),
    ]
    language = models.ForeignKey('Language', on_delete=models.CASCADE)
    term = models.CharField(max_length=255)
    translation = models.CharField(max_length=255)
    part_of_speech = models.CharField(max_length=20, choices=POS_CHOICES, default='other')
    example = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['language', 'term', 'translation'], name='uq_word_lang_term_translation')
        ]

    def __str__(self):
        return f"{self.term} → {self.translation}"

class Lesson(models.Model):
    language = models.ForeignKey('Language', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    words = models.ManyToManyField('Word', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['language', 'title'], name='uq_lesson_lang_title')
        ]

    def __str__(self):
        return self.title

class PracticeSession(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    language = models.ForeignKey('Language', on_delete=models.CASCADE)
    lesson = models.ForeignKey('Lesson', on_delete=models.SET_NULL, null=True, blank=True)
    question_count = models.PositiveSmallIntegerField()
    correct_count = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Session {self.id}"

class PracticeQuestion(models.Model):
    QTYPE_CHOICES = [
        ('term_to_translation', 'Term → Translation'),
        ('translation_to_term', 'Translation → Term'),
        ('multiple_choice', 'Multiple Choice'),
    ]
    session = models.ForeignKey('PracticeSession', on_delete=models.CASCADE)
    word = models.ForeignKey('Word', on_delete=models.CASCADE)
    qtype = models.CharField(max_length=30, choices=QTYPE_CHOICES)
    user_answer = models.CharField(max_length=255, blank=True)
    is_correct = models.BooleanField(default=False)
    options = models.TextField(blank=True)  
    def __str__(self):
        return f"{self.qtype}: {self.word}"
