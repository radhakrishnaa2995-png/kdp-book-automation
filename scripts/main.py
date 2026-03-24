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
    parser.add_argument("--puzzle-plan", default=DEFAULT_PUZZLE_PLAN)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--output-dir", default="output")
    parser.add_argument("--prefix", default="kdp_word_search")
    parser.add_argument("--theme-api-url", default=None)
    parser.add_argument("--openrouter-model", default=None)
    parser.add_argument("--comfyui-url", default=None)
    parser.add_argument("--comfyui-workflow", default=None)
    parser.add_argument("--comfyui-checkpoint", default="v1-5-pruned-emaonly.ckpt")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    puzzle_counts = parse_puzzle_plan(args.puzzle_plan)
    comfyui_workflow = args.comfyui_workflow
    if comfyui_workflow is None:
        local_workflow = Path(__file__).resolve().parent / "comfyui_workflow.json"
        if local_workflow.exists():
            comfyui_workflow = str(local_workflow)
            print(f"ℹ️ Using local ComfyUI workflow: {comfyui_workflow}")

    if len(puzzle_counts) == 1:
        output_file = os.path.join(args.output_dir, f"{args.prefix}_01_{puzzle_counts[0]}p.pdf")
        result = build_pdf(
            output_file=output_file,
            puzzle_count=puzzle_counts[0],
            seed=args.seed,
            theme_api_url=args.theme_api_url,
            openrouter_model=args.openrouter_model,
            comfyui_url=args.comfyui_url,
            comfyui_workflow=comfyui_workflow,
            comfyui_checkpoint=args.comfyui_checkpoint,
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
        comfyui_url=args.comfyui_url,
        comfyui_workflow=comfyui_workflow,
        comfyui_checkpoint=args.comfyui_checkpoint,
    )
    print(f"✅ Generated {len(batch.files)} unique PDFs")


if __name__ == "__main__":
    main()
