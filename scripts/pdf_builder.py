from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from comfyui_client import ComfyUIClient
import json
import os

def draw_theme_clipart(pdf_canvas, image_path, x=100, y=400, width=300, height=300):
    if not image_path or not os.path.exists(image_path):
        print("⚠️ No image found, skipping...")
        return

    try:
        img = ImageReader(image_path)
        pdf_canvas.drawImage(img, x, y, width, height)
    except Exception as e:
        print("Error drawing image:", e)


def build_pdf(
    output_file="output.pdf",
    puzzle_count=10,
    comfyui_url="http://127.0.0.1:8188"  # ✅ ALWAYS SET
):
    print("Using ComfyUI URL:", comfyui_url)

    pdf = canvas.Canvas(output_file, pagesize=letter)
    width, height = letter

    # Load workflow JSON
    with open("workflow.json", "r") as f:
        workflow = json.load(f)

    # Initialize ComfyUI client
    comfyui_client = ComfyUIClient(base_url=comfyui_url)

    for i in range(puzzle_count):
        prompt = f"Cute cartoon sticker, theme {i+1}, colorful, kids friendly"

        print(f"Generating image {i+1}...")

        try:
            image_path = comfyui_client.generate_image(workflow, prompt)
            print("Image saved at:", image_path)
        except Exception as e:
            print("❌ Image generation failed:", e)
            image_path = None

        # Draw on PDF
        draw_theme_clipart(pdf, image_path)

        pdf.drawString(100, 750, f"Puzzle Page {i+1}")
        pdf.showPage()

    pdf.save()
    print("✅ PDF created:", output_file)
