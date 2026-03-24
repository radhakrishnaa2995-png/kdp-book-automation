import json
import os

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader

from app.comfyui_client import ComfyUIClient


def draw_image(pdf, image_path):
    if not image_path or not os.path.exists(image_path):
        print("⚠️ Image missing, skipping...")
        return

    try:
        img = ImageReader(image_path)
        pdf.drawImage(img, 100, 400, width=300, height=300)
    except Exception as e:
        print("Error drawing image:", e)


def build_pdf(
    output_file="output.pdf",
    puzzle_count=10,
    comfyui_url="http://127.0.0.1:8188",
    workflow_path="workflow.json"
):
    print(f"Using ComfyUI: {comfyui_url}")

    # Load workflow
    if not os.path.exists(workflow_path):
        raise FileNotFoundError("workflow.json not found")

    with open(workflow_path, "r") as f:
        workflow = json.load(f)

    client = ComfyUIClient(comfyui_url)

    pdf = canvas.Canvas(output_file, pagesize=letter)

    for i in range(puzzle_count):
        prompt = f"Cute cartoon sticker, theme {i+1}, colorful, kids style"

        print(f"Generating image {i+1}...")

        try:
            # IMPORTANT: copy workflow each time
            image_path = client.generate_image(workflow.copy(), prompt)
            print("✔ Image:", image_path)
        except Exception as e:
            print("❌ Generation failed:", e)
            image_path = None

        draw_image(pdf, image_path)

        pdf.drawString(100, 750, f"Puzzle Page {i+1}")
        pdf.showPage()

    pdf.save()
    print(f"✅ PDF created: {output_file}")
