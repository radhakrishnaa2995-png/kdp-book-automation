from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader

import json
import os

from core.comfyui_client import ComfyUIClient


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
    comfyui_url="http://127.0.0.1:8188"
):
    print("Using ComfyUI:", comfyui_url)

    pdf = canvas.Canvas(output_file, pagesize=letter)

    # Load workflow
    with open("workflow.json", "r") as f:
        workflow = json.load(f)

    client = ComfyUIClient(base_url=comfyui_url)

    for i in range(puzzle_count):
        prompt = f"Cute cartoon sticker, theme {i+1}, colorful, kids style"

        print(f"Generating {i+1}...")

        try:
            image_path = client.generate_image(workflow, prompt)
            print("Image:", image_path)
        except Exception as e:
            print("❌ Failed:", e)
            image_path = None

        draw_image(pdf, image_path)

        pdf.drawString(100, 750, f"Puzzle Page {i+1}")
        pdf.showPage()

    pdf.save()
    print("✅ PDF created:", output_file)
