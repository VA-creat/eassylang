#  EassyLang

EassyLang — это простой тренажёр для изучения иностранных слов, созданный на Django.
Добавляйте новые слова, объединяйте их в уроки и тренируйтесь в удобной форме.


## Локальный запуск

```bash
# 1. Создайте виртуальное окружение
python -m venv .venv
source .venv/bin/activate   # для windows: .venv\Scripts\activate

# 2. Установите зависимости
pip install -r requirements.txt

# 3. Подготовьте базу данных
python manage.py migrate

# 4. Загрузите демо-данные (чтобы сразу были тестовые языки, слова и уроки)
python manage.py loaddata demo_data

# 5. Запустите сервер
python manage.py runserver
```

Откройте в браузере ссылку  http://127.0.0.1:8000/ 

---
## Возможности

* **Библиотека слов**: добавляйте новые слова вручную или импортируйте из CSV.
*  **Уроки**: объединяйте слова в тематические наборы.
*  **Тренировки**: проверяйте себя в разных режимах (слово → перевод, перевод → слово, multiple choice).
*  **Результаты**: получайте мгновенную обратную связь и мотивацию.

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

##  Панель админа

Есть возмодность управлять набором слов и уроками через панель администратора
Для этого создайте аккаунт админа:

```bash
python manage.py createsuperuser
```

и заходите на http://127.0.0.1:8000/admin/

---

##  Проверка качества кода

Запуск:

```bash
pylint langtrainer trainer manage.py --load-plugins=pylint_django
```
