import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from puzzles import generate_word_search, generate_words, generate_sudoku
from pdf_builder import create_pdf

def generate_book(theme, index):
    os.makedirs("outputs", exist_ok=True)

    words = generate_words(theme)

    puzzles = []

    # Add word search
    for _ in range(3):
        puzzles.append(generate_word_search(words))

    # Add sudoku
    puzzles.append(generate_sudoku())

    filename = f"outputs/{theme.replace(' ', '_')}_{index}.pdf"

    create_pdf(filename, f"{theme} Fun Book", puzzles)

    return filename
