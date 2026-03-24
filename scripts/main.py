import argparse
import os
import sys

# ✅ Ensure root directory is in Python path (fixes import issues everywhere)
ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from app.pdf_builder import build_pdf


def check_comfyui(url: str) -> bool:
    """Check if ComfyUI server is running"""
    try:
        import requests
        res = requests.get(url, timeout=3)
        return res.status_code == 200
    except Exception:
        return False


def main():
    parser = argparse.ArgumentParser(
        description="KDP Puzzle Book Generator with AI Stickers (ComfyUI)"
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
        help="Number of pages to generate"
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
        help="Path to workflow JSON"
    )

    args = parser.parse_args()

    # ✅ Resolve absolute paths
    workflow_path = os.path.abspath(args.workflow)
    output_path = os.path.abspath(args.output)

    print("📁 Project root:", ROOT_DIR)
    print("📄 Workflow:", workflow_path)
    print("🖨 Output:", output_path)
    print("🌐 ComfyUI:", args.comfyui)
    print()

    # ❌ Check workflow file
    if not os.path.exists(workflow_path):
        print("❌ ERROR: workflow.json not found")
        sys.exit(1)

    # ❌ Check ComfyUI server
    print("🔍 Checking ComfyUI server...")
    if not check_comfyui(args.comfyui):
        print("❌ ERROR: ComfyUI is not running or unreachable")
        print("👉 Start it inside ComfyUI folder:")
        print("   python main.py")
        sys.exit(1)

    print("✅ ComfyUI is running\n")

    # 🚀 Generate PDF
    try:
        print("🚀 Generating PDF...\n")

        build_pdf(
            output_file=output_path,
            puzzle_count=args.count,
            comfyui_url=args.comfyui,
            workflow_path=workflow_path
        )

        print("\n🎉 SUCCESS: PDF generated at", output_path)

    except Exception as e:
        print("\n❌ ERROR during generation:")
        print(e)
        sys.exit(1)


if __name__ == "__main__":
    main()
