from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch

WIDTH, HEIGHT = letter

def create_pdf(filename, title, puzzles):
    c = canvas.Canvas(filename, pagesize=letter)

    # 🎨 COVER PAGE
    c.setFillColor(colors.pink)
    c.setFont("Helvetica-Bold", 36)
    c.drawCentredString(WIDTH/2, HEIGHT-200, title)

    c.setFont("Helvetica", 18)
    c.setFillColor(colors.blue)
    c.drawCentredString(WIDTH/2, HEIGHT-250, "Fun Learning for Kids 🎉")

    c.showPage()

    # 🧩 PUZZLE PAGES
    for idx, grid in enumerate(puzzles):
        c.setFillColor(colors.black)
        c.setFont("Helvetica-Bold", 20)
        c.drawString(50, HEIGHT-50, f"Puzzle {idx+1}")

        y = HEIGHT - 120
        c.setFont("Courier-Bold", 18)

        for row in grid:
            c.drawString(100, y, "  ".join(row))
            y -= 25

        c.showPage()

    c.save()
