import os
from grid import generate_grid
from pdf_builder import create_pdf

def get_words(theme):
    base = {
        "Animals": ["CAT","DOG","LION","TIGER","ZEBRA"],
        "Fruits": ["APPLE","MANGO","BANANA","GRAPE"],
    }
    return base.get(theme, ["FUN","PLAY","GAME"])


def generate_book(theme, total):
    puzzles = []
    solutions = []

    for i in range(total):
        if i < total * 0.3:
            size, level = 8, "easy"
        elif i < total * 0.7:
            size, level = 10, "medium"
        else:
            size, level = 12, "hard"

        words = get_words(theme)
        grid, highlight = generate_grid(words, size)

        puzzles.append((grid, words, level))
        solutions.append((grid, words, highlight))

    os.makedirs("output", exist_ok=True)
    file = f"output/{theme}.pdf"

    create_pdf(file, theme, puzzles, solutions)

    return file
