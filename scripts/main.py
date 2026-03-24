import sys
import os

# ✅ Fix import path (VERY IMPORTANT)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import argparse
from core.pdf_builder import build_pdf


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--output", default="output.pdf")
    parser.add_argument("--count", type=int, default=10)
    parser.add_argument("--comfyui", default="http://127.0.0.1:8188")

    args = parser.parse_args()

    # Check workflow exists
    if not os.path.exists("workflow.json"):
        print("❌ workflow.json not found")
        return

    print("🚀 Starting generation...")

    build_pdf(
        output_file=args.output,
        puzzle_count=args.count,
        comfyui_url=args.comfyui
    )

    print("🎉 Done!")


if __name__ == "__main__":
    main()
