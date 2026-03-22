from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors

WIDTH, HEIGHT = A4


def draw_grid(c, grid, size, highlight=None):
    cell = 30
    start_x = (WIDTH - size * cell) / 2
    start_y = HEIGHT - 180

    c.setFont("Helvetica-Bold", 16)

    for i in range(size):
        for j in range(size):
            x = start_x + j * cell
            y = start_y - i * cell

            # Highlight solution
            if highlight and (i, j) in highlight:
                c.setFillColor(colors.yellow)
                c.rect(x, y, cell, cell, fill=1)
                c.setFillColor(colors.black)
            else:
                c.rect(x, y, cell, cell)

            c.drawCentredString(x + cell/2, y + 8, str(grid[i][j]))


def draw_words(c, words):
    c.setFont("Helvetica-Bold", 12)

    x = 50
    y = 120

    for word in words:
        c.setFillColor(colors.lightblue)
        c.roundRect(x, y, 110, 30, 8, fill=1)

        c.setFillColor(colors.black)
        c.drawCentredString(x + 55, y + 10, word)

        x += 120
        if x > WIDTH - 120:
            x = 50
            y -= 40


def create_pdf(filename, theme, puzzles, solutions):
    c = canvas.Canvas(filename, pagesize=A4)

    # 🎨 COVER PAGE
    c.setFillColor(colors.pink)
    c.rect(0, 0, WIDTH, HEIGHT, fill=1)

    c.setFillColor(colors.darkblue)
    c.setFont("Helvetica-Bold", 36)
    c.drawCentredString(WIDTH/2, HEIGHT-200, f"{theme} Puzzle Book")

    c.setFont("Helvetica", 18)
    c.drawCentredString(WIDTH/2, HEIGHT-250, "Fun Activities for Kids")

    c.showPage()

    # 🧩 PUZZLES
    for i, (grid, words, size) in enumerate(puzzles):
        c.setFont("Helvetica-Bold", 18)
        c.drawString(50, HEIGHT-50, f"Puzzle {i+1}")

        draw_grid(c, grid, size)
        draw_words(c, words)

        c.setFont("Helvetica", 10)
        c.drawString(WIDTH/2 - 20, 20, str(i+1))

        c.showPage()

    # ✅ SOLUTIONS
    for i, (grid, words, size, highlight) in enumerate(solutions):
        c.setFont("Helvetica-Bold", 18)
        c.drawString(50, HEIGHT-50, f"Solution {i+1}")

        draw_grid(c, grid, size, highlight)

        c.showPage()

    c.save()
