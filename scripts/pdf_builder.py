from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors

WIDTH, HEIGHT = letter


def create_pdf(filename, title, puzzles):
    c = canvas.Canvas(filename, pagesize=letter)

    # 🎨 COVER PAGE
    c.setFillColor(colors.pink)
    c.setFont("Helvetica-Bold", 34)
    c.drawCentredString(WIDTH / 2, HEIGHT - 200, title)

    c.setFont("Helvetica", 18)
    c.setFillColor(colors.blue)
    c.drawCentredString(WIDTH / 2, HEIGHT - 250, "Fun Learning for Kids 🎉")

    c.setFillColor(colors.green)
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(WIDTH / 2, HEIGHT - 300, "Word Search • Sudoku • Activities")

    c.showPage()

    # 🧩 PUZZLE PAGES
    for idx, grid in enumerate(puzzles):

        # Title
        c.setFillColor(colors.black)
        c.setFont("Helvetica-Bold", 22)
        c.drawString(50, HEIGHT - 60, f"Puzzle {idx + 1}")

        # Grid / Content
        y = HEIGHT - 120
        c.setFont("Courier-Bold", 18)

        for row in grid:
            # 🔥 FIX: convert everything to string
            row_text = "  ".join(map(str, row))
            c.drawString(80, y, row_text)
            y -= 25

        c.showPage()

    c.save()
