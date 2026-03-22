import sys
import os
import random
import json

# 🔥 Fix path for GitHub Actions
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

from generator import generate_book


def load_themes():
    themes_path = os.path.join(BASE_DIR, "..", "templates", "themes.json")

    try:
        with open(themes_path) as f:
            return json.load(f)
    except:
        # fallback themes
        return ["Wild Animals", "Fruits", "Pets", "School"]


def main():
    print("🔥 KDP BOOK GENERATION STARTED")

    themes = load_themes()

    total_books = 20  # ✅ number of books

    for i in range(total_books):
        theme = random.choice(themes)

        print(f"\n📘 Creating Book {i+1}: {theme}")

        # Each book has 50 puzzles (you can change)
        file = generate_book(theme, 50)

        print(f"✅ Generated: {file}")

    print("\n🎉 ALL BOOKS GENERATED SUCCESSFULLY!")


if __name__ == "__main__":
    main()
