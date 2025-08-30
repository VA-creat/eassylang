import csv
from io import TextIOWrapper

from django.contrib import messages
from django.db import transaction
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render

from .models import Language, Word, Lesson, PracticeSession, PracticeQuestion
from .forms import WordForm, LessonForm, CSVImportForm, PracticeStartForm
from .helpers import pick_words, mc_options_for, normalize_answer

def dashboard(request):
    ctx = {
        'lang_count': Language.objects.count(),
        'word_count': Word.objects.count(),
        'lesson_count': Lesson.objects.count(),
        'recent_sessions': PracticeSession.objects.order_by('-created_at')[:5],
    }
    return render(request, 'trainer/dashboard.html', ctx)

def word_list(request):
    qs = Word.objects.select_related('language').all().order_by('language__name', 'term')
    lang_id = request.GET.get('language')
    q = (request.GET.get('q') or '').strip()
    if lang_id:
        qs = qs.filter(language_id=lang_id)
    if q:
        qs = qs.filter(Q(term__icontains=q) | Q(translation__icontains=q))
    ctx = {
        'words': qs,
        'languages': Language.objects.all(),
        'current_language': int(lang_id) if lang_id else None,
        'query': q,
    }
    return render(request, 'trainer/word_list.html', ctx)

def word_add(request):
    if request.method == 'POST':
        form = WordForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Готово! Слово сохранено ')
            return redirect('word_list')
    else:
        form = WordForm()
    return render(request, 'trainer/word_form.html', {'form': form})

def lesson_list(request):
    lessons = Lesson.objects.select_related('language').annotate(word_count=Count('words')).order_by('language__name', 'title')
    return render(request, 'trainer/lesson_list.html', {'lessons': lessons})

def lesson_detail(request, lesson_id):
    lesson = get_object_or_404(Lesson.objects.select_related('language').prefetch_related('words'), pk=lesson_id)
    return render(request, 'trainer/lesson_detail.html', {'lesson': lesson})

def lesson_add(request):
    if request.method == 'POST':
        form = LessonForm(request.POST)
        if form.is_valid():
            lesson = form.save()
            messages.success(request, 'Урок создан!')
            return redirect('lesson_detail', lesson_id=lesson.id)
    else:
        form = LessonForm()
    return render(request, 'trainer/lesson_form.html', {'form': form})

def import_csv(request):
    if request.method == 'POST':
        form = CSVImportForm(request.POST, request.FILES)
        if form.is_valid():
            lang = form.cleaned_data['language']
            fobj = form.cleaned_data['file']
            added = 0
            skipped = 0
            wrapper = TextIOWrapper(fobj.file, encoding='utf-8', errors='ignore')
            reader = csv.reader(wrapper)
            with transaction.atomic():
                for row in reader:
                    if not row or all(not (c or '').strip() for c in row):
                        continue
                    term = (row[0] if len(row) > 0 else '').strip()
                    translation = (row[1] if len(row) > 1 else '').strip()
                    pos = (row[2] if len(row) > 2 else 'other').strip() or 'other'
                    example = (row[3] if len(row) > 3 else '').strip()
                    if not term or not translation:
                        skipped += 1
                        continue
                    if Word.objects.filter(language=lang, term=term, translation=translation).exists():
                        skipped += 1
                        continue
                    Word.objects.create(language=lang, term=term, translation=translation, part_of_speech=pos, example=example)
                    added += 1
            messages.success(request, f'Импорт готов: добавлено {added}, пропущено {skipped}.')
            return redirect('word_list')
    else:
        form = CSVImportForm()
    return render(request, 'trainer/import_form.html', {'form': form})

def practice_start(request):
    if request.method == 'POST':
        form = PracticeStartForm(request.POST)
        if form.is_valid():
            language = form.cleaned_data['language']
            lesson = form.cleaned_data.get('lesson')
            qcount = form.cleaned_data['question_count']
            include_mc = form.cleaned_data['include_multiple_choice']

            if lesson:
                pool = lesson.words.all()
            else:
                pool = Word.objects.filter(language=language)
            chosen = pick_words(pool, qcount)
            if not chosen:
                messages.error(request, 'Пока нет слов для такой настройки. Добавь парочку и попробуй снова ')
                return redirect('practice_start')

            session = PracticeSession.objects.create(language=language, lesson=lesson, question_count=len(chosen))
            for idx, w in enumerate(chosen):
                if include_mc and idx % 3 == 2:
                    options = mc_options_for(w, pool)
                    PracticeQuestion.objects.create(session=session, word=w, qtype='multiple_choice', options='||'.join(options))
                elif idx % 2 == 0:
                    PracticeQuestion.objects.create(session=session, word=w, qtype='term_to_translation')
                else:
                    PracticeQuestion.objects.create(session=session, word=w, qtype='translation_to_term')
            return redirect('practice_run', session_id=session.id)
    else:
        form = PracticeStartForm()
    return render(request, 'trainer/practice_start.html', {'form': form})

def _get_next_unanswered(session):
    return PracticeQuestion.objects.filter(session=session, user_answer='').order_by('id').first()

def practice_run(request, session_id):
    session = get_object_or_404(PracticeSession, pk=session_id)
    question = _get_next_unanswered(session)
    if not question:
        return redirect('practice_result', session_id=session.id)

    options = question.options.split('||') if question.qtype == 'multiple_choice' and question.options else []

    if request.method == 'POST':
        user_answer = (request.POST.get('answer') or '').strip()
        if question.qtype == 'term_to_translation':
            correct = normalize_answer(user_answer) == normalize_answer(question.word.translation)
        elif question.qtype == 'translation_to_term':
            correct = normalize_answer(user_answer) == normalize_answer(question.word.term)
        else:
            correct = normalize_answer(user_answer) == normalize_answer(question.word.translation)

        question.user_answer = user_answer
        question.is_correct = bool(correct)
        question.save()

    
        if not _get_next_unanswered(session):
            session.correct_count = PracticeQuestion.objects.filter(session=session, is_correct=True).count()
            session.save()
            return redirect('practice_result', session_id=session.id)

        return redirect('practice_run', session_id=session.id)

    total = session.question_count
    answered = PracticeQuestion.objects.filter(session=session).exclude(user_answer='').count()
    current_index = answered + 1
    progress_pct = int((answered / total) * 100) if total else 0
    return render(request, 'trainer/practice_run.html', {'session': session, 'question': question, 'options': options, 'total': total, 'current_index': current_index, 'progress_pct': progress_pct})

def practice_result(request, session_id):
    session = get_object_or_404(PracticeSession, pk=session_id)
    questions = PracticeQuestion.objects.filter(session=session).select_related('word')
    incorrect = [q for q in questions if not q.is_correct]
    total = session.question_count or 1
    pct = int((session.correct_count / total) * 100)
    if pct == 100:
        mood = 'Идеально! Можно повышать уровень.'
    elif pct >= 80:
        mood = 'Отличный результат! Ещё немного, и будет 100% верно!'
    elif pct >= 50:
        mood = 'Неплохо! Пара повторений и станет лучше.'
    else:
        mood = 'Попробуй короткие уроки и повторение.'
    return render(request, 'trainer/practice_result.html', {'session': session, 'questions': questions, 'incorrect': incorrect, 'mood_message': mood})
