import os
import sys

# Fix import path for GitHub Actions
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from puzzles import generate_word_search, generate_words
from pdf_builder import create_pdf


def generate_book(theme, index):
    # Ensure outputs folder exists
    os.makedirs("outputs", exist_ok=True)

    # Get words based on theme
    words = generate_words(theme)

    # Generate puzzles
    puzzles = []
    for _ in range(5):  # 5 pages per book
        grid = generate_word_search(words)
        puzzles.append(grid)

    # Clean filename
    safe_theme = theme.replace(" ", "_")

    filename = f"outputs/{safe_theme}_{index}.pdf"

    # Create PDF
    create_pdf(filename, f"{theme} Activity Book", puzzles)

    print(f"✅ Created: {filename}")

    return filename
