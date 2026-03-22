import os
from puzzles import generate_word_search
from pdf_builder import create_pdf


def get_words(level):
    if level == "easy":
        return ["CAT", "DOG", "SUN", "BAT"]
    elif level == "medium":
        return ["TIGER", "MANGO", "ZEBRA"]
    else:
        return ["ELEPHANT", "KANGAROO", "RHINOCEROS"]


def generate_book(theme, total):
    os.makedirs("outputs", exist_ok=True)

    puzzles = []
    solutions = []

    for i in range(total):

        if i < total * 0.3:
            level = "easy"
            size = 8
        elif i < total * 0.7:
            level = "medium"
            size = 10
        else:
            level = "hard"
            size = 12

        words = get_words(level)

        grid, highlight = generate_word_search(words, size)

        puzzles.append((grid, words, size))
        solutions.append((grid, words, size, highlight))

    filename = f"outputs/{theme}.pdf"

    create_pdf(filename, theme, puzzles, solutions)

    return filename
