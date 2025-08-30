#  EassyLang

EassyLang — это простой тренажёр для изучения иностранных слов, созданный на Django.
Добавляй новые слова, объединяй их в уроки и тренируйся в удобной форме.


## Запуск локально

```bash
# 1. Создай виртуальное окружение
python -m venv .venv
source .venv/bin/activate   # для windows: .venv\Scripts\activate

# 2. Установи зависимости
pip install -r requirements.txt

# 3. Подготовить базу данных
python manage.py migrate

# 4. Загрузить демо-данные (чтобы сразу были языки, слова и уроки)
python manage.py loaddata demo_data

# 5. Запустить сервер
python manage.py runserver
```

Открой в браузере ссылку  http://127.0.0.1:8000/ 

---
## Возможности

* **Библиотека слов**: добавляй новые слова вручную или импортируй из CSV.
*  **Уроки**: объединяй слова в тематические наборы.
*  **Тренировки**: проверяй себя в разных режимах (слово → перевод, перевод → слово, multiple choice).
*  **Результаты**: получай мгновенную обратную связь и мотивацию.

---

##  Импорт CSV

Поддерживается импорт слов из CSV ( UTF-8).

**Формат строк:**

```
term,translation,part_of_speech,example
apple,яблоко,noun,An apple a day keeps the doctor away
book,книга,noun,
thank you,спасибо,phrase,
```

* `term` — слово/фраза на изучаемом языке
* `translation` — перевод
* `part_of_speech` — часть речи (`noun`, `verb`, `adj`, `adv`, `phrase`)
* `example` — пример использования (опционально)

---

##  Админка

Хочешь управлять словами и уроками через интерфейс администратора?
Создай аккаунт админа:

```bash
python manage.py createsuperuser
```

и заходи на http://127.0.0.1:8000/admin/

---

##  Проверка качества кода

Запуск:

```bash
pylint langtrainer trainer manage.py --load-plugins=pylint_django
```
