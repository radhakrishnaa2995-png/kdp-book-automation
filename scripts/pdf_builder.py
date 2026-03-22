from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from layout import get_grid_layout

# ✅ REGISTER CUSTOM FONT (VERY IMPORTANT)
pdfmetrics.registerFont(
    TTFont("KidFont", "assets/fonts/Fredoka.ttf")
)

WIDTH, HEIGHT = A4


def draw_page_number(c, num):
    c.setFont("KidFont", 10)
    c.drawCentredString(WIDTH / 2, 20, str(num))


def draw_title_page(c, theme):
    c.setFont("KidFont", 36)
    c.drawCentredString(WIDTH / 2, HEIGHT - 250, f"{theme}")

    c.setFont("KidFont", 18)
    c.drawCentredString(WIDTH / 2, HEIGHT - 300, "Fun Puzzle Book for Kids")

    # simple decorative elements
    c.circle(100, 700, 20, fill=1)
    c.circle(500, 700, 20, fill=1)


def draw_grid(c, grid, highlight=None):
    size = len(grid)
    cell, start_x, start_y = get_grid_layout(size)

    c.setFont("KidFont", cell * 0.5)

    for i in range(size):
        for j in range(size):
            x = start_x + j * cell
            y = start_y - i * cell

            if highlight and (i, j) in highlight:
                c.setFillColor(colors.yellow)
                c.rect(x, y, cell, cell, fill=1)
                c.setFillColor(colors.black)

            c.rect(x, y, cell, cell)
            c.drawCentredString(x + cell / 2, y + cell / 4, grid[i][j])


def draw_words(c, words):
    cols = 3
    spacing = 150
    x_start = 80
    y = 120

    c.setFont("KidFont", 12)

    for i, word in enumerate(words):
        col = i % cols
        row = i // cols

        x = x_start + col * spacing
        y_pos = y - row * 40

        c.roundRect(x, y_pos, 120, 25, 6, fill=0)
        c.drawCentredString(x + 60, y_pos + 8, word)


def create_pdf(file, theme, puzzles, solutions):
    c = canvas.Canvas(file, pagesize=A4)

    # Title Page
    draw_title_page(c, theme)
    c.showPage()

    page_num = 1

    # Puzzle Pages
    for i, (grid, words, level) in enumerate(puzzles):
        c.setFont("KidFont", 16)
        c.drawString(50, HEIGHT - 50, f"Puzzle {i+1} ({level.upper()})")

        draw_grid(c, grid)
        draw_words(c, words)

        draw_page_number(c, page_num)
        page_num += 1

        c.showPage()

    # Solutions Pages
    for i, (grid, words, highlight) in enumerate(solutions):
        c.setFont("KidFont", 16)
        c.drawString(50, HEIGHT - 50, f"Solution {i+1}")

        draw_grid(c, grid, highlight)
        draw_page_number(c, page_num)

        page_num += 1
        c.showPage()

    c.save()
