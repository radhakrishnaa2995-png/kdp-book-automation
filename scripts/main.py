import sys
import os

print("🔥 SCRIPT STARTED")

# Fix path for GitHub Actions
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

import json
import random
from generator import generate_book


def load_themes():
    themes_path = os.path.join(BASE_DIR, "..", "templates", "themes.json")
    print("📂 Loading themes from:", themes_path)

    with open(themes_path) as f:
        return json.load(f)


def main():
    print("🚀 INSIDE MAIN FUNCTION")

    themes = load_themes()
    print("🎯 Themes loaded:", themes)

    total_books = 20   # 🔥 CHANGE HERE (20 books)

    for i in range(total_books):
        theme = random.choice(themes)
        print(f"\n📘 Creating Book {i+1} with theme: {theme}")

        file = generate_book(theme, i)

        print(f"✅ Generated: {file}")

    print("\n🎉 ALL BOOKS GENERATED SUCCESSFULLY!")


if __name__ == "__main__":
    main()
