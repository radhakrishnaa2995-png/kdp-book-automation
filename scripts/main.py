from __future__ import annotations

import argparse
import os

from pdf_builder import build_pdf


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a KDP-ready themed word search puzzle book.")
    parser.add_argument("--puzzles", type=int, default=24, help="Number of puzzle pages to generate.")
    parser.add_argument("--seed", type=int, default=20260322, help="Random seed for reproducible books.")
    parser.add_argument(
        "--output",
        default=os.path.join("output", "kdp_word_search_book.pdf"),
        help="Output PDF path.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = build_pdf(output_file=args.output, puzzle_count=args.puzzles, seed=args.seed)
    print(f"✅ Generated {len(result.puzzles)} unique puzzle pages")
    print(f"✅ PDF saved to: {result.output_file}")


if __name__ == "__main__":
    main()
