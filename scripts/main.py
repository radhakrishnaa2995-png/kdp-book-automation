from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path
from typing import List

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from scripts.pdf_builder import build_pdf, build_pdf_batch
else:
    from .pdf_builder import build_pdf, build_pdf_batch

DEFAULT_PUZZLE_PLAN = "25,50,25,50,25,50,25,50,25,50,25,50,25,50,25,50,25,50,25,50"



def parse_puzzle_plan(raw_plan: str) -> List[int]:
    values = []
    for item in raw_plan.split(","):
        clean = item.strip()
        if not clean:
            continue
        values.append(int(clean))
    if not values:
        raise ValueError("Puzzle plan cannot be empty.")
    return values



def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate KDP-ready themed word search puzzle PDFs.")
    parser.add_argument(
        "--puzzle-plan",
        default=DEFAULT_PUZZLE_PLAN,
        help=(
            "Comma-separated puzzle counts per PDF. Default creates 20 PDFs total: "
            "10 books with 25 puzzles and 10 books with 50 puzzles in alternating order."
        ),
    )
    parser.add_argument("--seed", type=int, default=None, help="Optional seed. Leave unset for a fresh batch every run.")
    parser.add_argument(
        "--output-dir",
        default="output",
        help="Directory where generated PDFs will be saved.",
    )
    parser.add_argument(
        "--prefix",
        default="kdp_word_search",
        help="Base filename prefix for generated PDFs.",
    )
    parser.add_argument(
        "--theme-api-url",
        default=None,
        help="Optional HTTP endpoint that returns fresh themes/words for every run.",
    )
    parser.add_argument(
        "--openrouter-model",
        default=None,
        help="Optional OpenRouter model slug, e.g. openai/gpt-4o-mini.",
    )
    return parser.parse_args()



def main() -> None:
    args = parse_args()
    puzzle_counts = parse_puzzle_plan(args.puzzle_plan)

    if len(puzzle_counts) == 1:
        output_file = os.path.join(args.output_dir, f"{args.prefix}_01_{puzzle_counts[0]}p.pdf")
        result = build_pdf(
            output_file=output_file,
            puzzle_count=puzzle_counts[0],
            seed=args.seed,
            theme_api_url=args.theme_api_url,
            openrouter_model=args.openrouter_model,
        )
        print(f"✅ Generated 1 unique PDF with {puzzle_counts[0]} puzzles")
        print(f"✅ PDF saved to: {result.output_file}")
        return

    batch = build_pdf_batch(
        output_dir=args.output_dir,
        puzzle_counts=puzzle_counts,
        seed=args.seed,
        prefix=args.prefix,
        theme_api_url=args.theme_api_url,
        openrouter_model=args.openrouter_model,
    )
    print(f"✅ Generated {len(batch.files)} unique PDFs")
    print(f"✅ Batch seed: {batch.batch_seed}")
    for path, book_seed, puzzle_count in zip(batch.files, batch.seeds, batch.puzzle_counts):
        print(f"✅ {path} ({puzzle_count} puzzles, seed={book_seed})")


if __name__ == "__main__":
    main()
