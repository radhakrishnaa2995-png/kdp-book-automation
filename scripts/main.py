from __future__ import annotations

import argparse
import os
from typing import List

from .pdf_builder import build_pdf, build_pdf_batch


DEFAULT_PUZZLE_PLAN = "25,50,25,50,25,50,25,50,25,50,25,50,25,50,25,50,25,50,25,50"


# --------------------------------------------------
# 🔹 HELPERS
# --------------------------------------------------

def parse_puzzle_plan(raw_plan: str) -> List[int]:
    values = []
    for item in raw_plan.split(","):
        item = item.strip()
        if item:
            values.append(int(item))

    if not values:
        raise ValueError("Puzzle plan cannot be empty.")

    return values


# --------------------------------------------------
# 🔹 ARGUMENTS
# --------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate KDP-ready word search puzzle PDFs"
    )

    parser.add_argument(
        "--puzzle-plan",
        default=DEFAULT_PUZZLE_PLAN,
        help="Comma-separated puzzle counts (each = 1 PDF)",
    )

    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Optional seed (leave empty for randomness)",
    )

    parser.add_argument(
        "--output-dir",
        default="output",
        help="Output folder",
    )

    parser.add_argument(
        "--prefix",
        default="kdp_word_search",
        help="File name prefix",
    )

    return parser.parse_args()


# --------------------------------------------------
# 🔹 MAIN
# --------------------------------------------------

def main() -> None:
    args = parse_args()

    puzzle_counts = parse_puzzle_plan(args.puzzle_plan)

    if len(puzzle_counts) == 1:
        output_file = os.path.join(
            args.output_dir,
            f"{args.prefix}_01_{puzzle_counts[0]}p.pdf",
        )

        result = build_pdf(
            output_file=output_file,
            puzzle_count=puzzle_counts[0],
            seed=args.seed,
        )

        print(f"✅ Generated 1 PDF")
        print(f"📄 {result.output_file}")
        return

    batch = build_pdf_batch(
        output_dir=args.output_dir,
        puzzle_counts=puzzle_counts,
        seed=args.seed,
        prefix=args.prefix,
    )

    print(f"✅ Generated {len(batch.files)} PDFs")
    print(f"🎯 Batch seed: {batch.batch_seed}")

    for path, seed, count in zip(batch.files, batch.seeds, batch.puzzle_counts):
        print(f"📄 {path} ({count} puzzles, seed={seed})")


# --------------------------------------------------

if __name__ == "__main__":
    main()
