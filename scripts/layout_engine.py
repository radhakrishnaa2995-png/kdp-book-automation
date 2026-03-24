LIGHT_PAGE_BACKGROUNDS = (
    colors.HexColor("#f8f1df"),
    colors.HexColor("#f3eefc"),
    colors.HexColor("#eef7f1"),
    colors.HexColor("#fff1f2"),
    colors.HexColor("#edf6ff"),
)

def draw_page_background(pdf_canvas, variant: int = 0) -> None:
    background = LIGHT_PAGE_BACKGROUNDS[variant % len(LIGHT_PAGE_BACKGROUNDS)]
    pdf_canvas.setFillColor(background)
    pdf_canvas.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, stroke=0, fill=1)

def draw_theme_clipart(pdf_canvas, image_path: str | None, layout: PageLayout) -> None:
    size = min(88.0, layout.grid.box_size * 0.16)
    top_y = layout.title_y - 12
    bottom_y = layout.words.y + 2
    positions = [
        (CONTENT_LEFT - 6, top_y),
        (CONTENT_RIGHT - size + 6, top_y),
        (CONTENT_LEFT - 6, bottom_y),
        (CONTENT_RIGHT - size + 6, bottom_y),
    ]
    if not image_path:
        return

    for x, y in positions:
        pdf_canvas.drawImage(image_path, x, y, width=size, height=size, preserveAspectRatio=True, mask="auto")
