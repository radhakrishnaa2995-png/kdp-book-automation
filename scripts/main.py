from generator import generate_book
from pdf_builder import build_pdf


def main():
    print("🔥 KDP BOOK GENERATION STARTED")

    # ✅ User inputs
    theme = "Animals"   # You can still type "Animals"
    puzzle_count = 50   # 25 / 50 / 75 / 100

    # ✅ Generate puzzles
    puzzles, solutions = generate_book(theme, puzzle_count)

    # ✅ Output file name
    output_file = f"{theme.replace(' ', '_')}_{puzzle_count}_puzzles.pdf"

    # ✅ Build PDF
    build_pdf(output_file, puzzles, solutions, theme)

    print(f"✅ Book Generated Successfully: {output_file}")


if __name__ == "__main__":
    main()
