import random
import json
import os
from grid import generate_puzzle


# ✅ LOAD THEMES (FIXED)
def load_themes():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    theme_path = os.path.join(base_dir, "..", "templates", "themes.json")

    if not os.path.exists(theme_path):
        raise FileNotFoundError(f"themes.json not found at {theme_path}")

    with open(theme_path, "r") as f:
        return json.load(f)


# ✅ DIFFICULTY LOGIC
def get_grid_size(index, total):
    progress = index / total

    if progress < 0.3:
        return 10  # EASY
    elif progress < 0.7:
        return 12  # MEDIUM
    else:
        return 15  # HARD


# ✅ WORD SELECTION (10–15 words)
def select_words(word_pool):
    num_words = random.randint(10, 15)

    # prevent crash if list small
    if len(word_pool) < num_words:
        num_words = len(word_pool)

    words = random.sample(word_pool, num_words)
    return [w.upper() for w in words]


# ✅ MAIN BOOK GENERATOR
def generate_book(theme_name="Farm Animals", puzzle_count=25):

    # 🔥 Load + normalize themes
    themes = load_themes()
    themes = {k.lower(): v for k, v in themes.items()}

    theme_name = theme_name.strip().lower()

    if theme_name not in themes:
        raise ValueError(f"Theme '{theme_name}' not found. Available: {list(themes.keys())}")

    word_pool = themes[theme_name]

    puzzles = []
    solutions = []

    for i in range(puzzle_count):
        size = get_grid_size(i, puzzle_count)

        # retry logic for better placement
        for _ in range(10):
            words = select_words(word_pool)
            grid, solution = generate_puzzle(words, size)

            if len(solution) >= max(5, len(words) - 2):
                break

        puzzles.append((grid, words))
        solutions.append((grid, solution))

    return puzzles, solutions
