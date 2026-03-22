import random
import json
import os
from grid import generate_puzzle


# 📂 Load themes from JSON
themes = load_themes()

# Normalize everything to lowercase
themes = {k.lower(): v for k, v in themes.items()}
theme_name = theme_name.strip().lower()

if theme_name not in themes:
    raise ValueError(f"Theme '{theme_name}' not found")

word_pool = themes[theme_name]


# 🎯 Difficulty settings
def get_grid_size(index, total):
    """Return grid size based on difficulty progression"""
    progress = index / total

    if progress < 0.3:
        return 10  # EASY
    elif progress < 0.7:
        return 12  # MEDIUM
    else:
        return 15  # HARD


# 🧠 Select words (10–15 words per puzzle)
def select_words(word_list):
    num_words = random.randint(10, 15)
    words = random.sample(word_list, num_words)
    return [w.upper() for w in words]


# 🔁 Generate full book
def generate_book(theme_name="Animals", puzzle_count=25):
    themes = load_themes()

    if theme_name not in themes:
        raise ValueError(f"Theme '{theme_name}' not found")

    word_pool = themes[theme_name]

    puzzles = []
    solutions = []

    for i in range(puzzle_count):
        size = get_grid_size(i, puzzle_count)

        # Keep trying until valid puzzle generated
        for _ in range(10):
            words = select_words(word_pool)
            grid, solution = generate_puzzle(words, size)

            if len(solution) >= 8:  # ensure enough words placed
                break

        puzzles.append((grid, words))
        solutions.append((grid, solution))

    return puzzles, solutions
