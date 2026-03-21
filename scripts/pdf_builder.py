from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

WIDTH, HEIGHT = letter

def create_pdf(filename, title, puzzles):
    c = canvas.Canvas(filename, pagesize=letter)

    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(WIDTH/2, HEIGHT-100, title)
    c.showPage()

    for idx, grid in enumerate(puzzles):
        c.setFont("Helvetica", 14)
        c.drawString(50, HEIGHT-50, f"Puzzle {idx+1}")

        y = HEIGHT - 100
        for row in grid:
            c.drawString(50, y, " ".join(row))
            y -= 20

        c.showPage()

    c.save()
