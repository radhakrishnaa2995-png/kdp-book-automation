import os
from generator import generate_book
from pdf_builder import build_pdf


def main():
    print("🔥 KDP BOOK GENERATION STARTED")

    # ✅ User inputs
    theme = "Animals"        # You can write: Animals / Farm Animals / pets etc.
    puzzle_count = 50        # Options: 25 / 50 / 75 / 100

    # ✅ Generate puzzles
    puzzles, solutions = generate_book(theme, puzzle_count)

    # ✅ Ensure output folder exists
    os.makedirs("output", exist_ok=True)

    # ✅ Output file path (VERY IMPORTANT for GitHub Actions)
    output_file = os.path.join(
        "output",
        f"{theme.replace(' ', '_')}_{puzzle_count}_puzzles.pdf"
    )

    # ✅ Build PDF
    build_pdf(output_file, puzzles, solutions, theme)

    print(f"✅ Book Generated Successfully: {output_file}")


if __name__ == "__main__":
    main()
