from django import forms
from .models import Word, Lesson, Language

class WordForm(forms.ModelForm):
    class Meta:
        model = Word
        fields = ['language', 'term', 'translation', 'part_of_speech', 'example']
        labels = {
            'language': 'Язык',
            'term': 'Слово',
            'translation': 'Перевод',
            'part_of_speech': 'Часть речи',
            'example': 'Пример (необязательно)',
        }
        widgets = {
            'term': forms.TextInput(attrs={'placeholder': 'apple / книга / gracias'}),
            'translation': forms.TextInput(attrs={'placeholder': 'яблоко / book / thank you'}),
            'example': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Короткий пример использования'}),
        }

    def clean(self):
        cleaned = super().clean()
        lang = cleaned.get('language')
        term = (cleaned.get('term') or '').strip()
        translation = (cleaned.get('translation') or '').strip()
        if lang and term and translation:
            exists = Word.objects.filter(language=lang, term=term, translation=translation).exists()
            if exists:
                raise forms.ValidationError('Такое слово уже есть (язык + слово + перевод).')
        return cleaned

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['language', 'title', 'description', 'words']
        labels = {
            'language': 'Язык',
            'title': 'Название урока',
            'description': 'Описание (необязательно)',
            'words': 'Слова для урока',
        }
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Например: Путешествия'}),
            'description': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Короткое описание темы'}),
        }

class CSVImportForm(forms.Form):
    language = forms.ModelChoiceField(queryset=Language.objects.all(), label='Язык')
    file = forms.FileField(label='CSV‑файл', help_text='CSV UTF‑8: term,translation,part_of_speech,example')

    def clean_file(self):
        f = self.cleaned_data['file']
        if f.size > 2 * 1024 * 1024:
            raise forms.ValidationError('Файл слишком большой. Максимум 2 МБ.')
        return f

class PracticeStartForm(forms.Form):
    language = forms.ModelChoiceField(queryset=Language.objects.all(), label='Язык')
    lesson = forms.ModelChoiceField(queryset=Lesson.objects.all(), required=False, label='Урок (необязательно)')
    question_count = forms.IntegerField(min_value=1, max_value=50, initial=10, label='Количество вопросов')
    include_multiple_choice = forms.BooleanField(required=False, initial=True, label='Добавлять вопросы с вариантами ответов')

    def clean(self):
        cleaned = super().clean()
        lang = cleaned.get('language')
        lesson = cleaned.get('lesson')
        if lesson and lang and lesson.language_id != lang.id:
            raise forms.ValidationError('Выбранный урок относится к другому языку.')
        return cleaned
