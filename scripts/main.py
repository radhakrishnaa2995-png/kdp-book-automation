import argparse
import os
from pdf_builder import build_pdf


def validate_comfyui(url: str):
    """Check if ComfyUI server is running"""
    import requests
    try:
        res = requests.get(url)
        return res.status_code == 200
    except Exception:
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Generate KDP Puzzle Book with AI Stickers"
    )

    parser.add_argument(
        "--output",
        type=str,
        default="output.pdf",
        help="Output PDF file name"
    )

    parser.add_argument(
        "--count",
        type=int,
        default=10,
        help="Number of puzzle pages"
    )

    parser.add_argument(
        "--comfyui",
        type=str,
        default="http://127.0.0.1:8188",
        help="ComfyUI server URL"
    )

    parser.add_argument(
        "--workflow",
        type=str,
        default="workflow.json",
        help="Path to workflow JSON file"
    )

    args = parser.parse_args()

    # ✅ Check workflow file
    if not os.path.exists(args.workflow):
        print(f"❌ ERROR: Workflow file not found: {args.workflow}")
        return

    # ✅ Check ComfyUI server
    print("🔍 Checking ComfyUI server...")
    if not validate_comfyui(args.comfyui):
        print("❌ ERROR: ComfyUI is not running.")
        print("👉 Start it using: python main.py (inside ComfyUI folder)")
        return

    print("✅ ComfyUI is running")

    # ✅ Generate PDF
    print("🚀 Starting PDF generation...")
    build_pdf(
        output_file=args.output,
        puzzle_count=args.count,
        comfyui_url=args.comfyui
    )

    print("🎉 DONE! Your PDF is ready.")


if __name__ == "__main__":
    main()
