import random
from .models import Word

def pick_words(words, n):
    pool = list(words)
    if n >= len(pool):
        random.shuffle(pool)
        return pool
    return random.sample(pool, n)

def mc_options_for(word, candidates):
    others = [w.translation for w in candidates if w.id != word.id and w.translation]
    if len(others) >= 3:
        distractors = random.sample(others, 3)
    else:
        distractors = others[:3]
    options = distractors + [word.translation]
    random.shuffle(options)
    return options

def normalize_answer(s):
    return (s or '').strip().lower()
