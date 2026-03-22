from generator import generate_book

def main():
    print("🔥 KDP BOOK GENERATION STARTED")

    theme = "Animals"   # Change theme here
    puzzles = 50        # Change number of puzzles here

    file = generate_book(theme, puzzles)

    print(f"✅ Book Generated Successfully: {file}")


if __name__ == "__main__":
    main()
