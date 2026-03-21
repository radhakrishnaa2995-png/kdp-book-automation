import os
from puzzles import generate_word_search, generate_words
from pdf_builder import create_pdf

def generate_book(theme, index):
    words = generate_words(theme)

    puzzles = []
    for _ in range(5):
        grid = generate_word_search(words)
        puzzles.append(grid)

    os.makedirs("outputs", exist_ok=True)

    filename = f"outputs/{theme.replace(' ', '_')}_{index}.pdf"

    create_pdf(filename, f"{theme} Activity Book", puzzles)

    return filename
