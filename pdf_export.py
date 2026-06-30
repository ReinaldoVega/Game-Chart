# pdf_export.py

from io import BytesIO
from reportlab.lib.pagesizes import landscape, letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from PIL import Image

from config import LOGO_PATH, MAX_ABS


NAVY = colors.HexColor("#0C2340")
ORANGE = colors.HexColor("#FA4616")
DARK = colors.HexColor("#111827")
MUTED = colors.HexColor("#667085")
GRID = colors.HexColor("#D0D5DD")
LIGHT = colors.HexColor("#F8FAFC")
SOFT_ORANGE = colors.HexColor("#FFF1EA")


def safe(value):
    return str(value or "").replace("\n", " ").strip()


def draw_logo(c, x, y, w, h):
    try:
        img = Image.open(LOGO_PATH).convert("RGBA")
        c.drawImage(ImageReader(img), x, y, width=w, height=h, mask="auto")
    except Exception:
        pass


def wrap_text(text, max_chars):
    text = safe(text)
    return [text[i:i + max_chars] for i in range(0, len(text), max_chars)]


def draw_diamond(c, x, y, size, result):
    result = safe(result)

    # Diamond points
    top = (x + size / 2, y + size)
    right = (x + size, y + size / 2)
    bottom = (x + size / 2, y)
    left = (x, y + size / 2)

    c.setStrokeColor(GRID)
    c.setLineWidth(0.8)

    c.line(*top, *right)
    c.line(*right, *bottom)
    c.line(*bottom, *left)
    c.line(*left, *top)

    filled_bases = []

    if result in ["1B", "BB", "HBP", "ROE", "FC"]:
        filled_bases = [right]
    elif result == "2B":
        filled_bases = [right, top]
    elif result == "3B":
        filled_bases = [right, top, left]
    elif result == "HR":
        filled_bases = [right, top, left, bottom]

    for bx, by in filled_bases:
        c.setFillColor(ORANGE)
        c.circle(bx, by, 2.7, fill=1, stroke=0)


def result_color(result):
    result = safe(result)

    if result in ["1B", "2B", "3B"]:
        return colors.HexColor("#15803D")
    if result == "HR":
        return ORANGE
    if result in ["BB", "HBP"]:
        return colors.HexColor("#2563EB")
    if result:
        return DARK

    return MUTED


def draw_ab_box(c, x, y, w, h, ab_num, data):
    result = safe(data.get("result"))
    pitch = safe(data.get("pitch"))
    velo = safe(data.get("velo"))
    count = safe(data.get("count"))
    zone = safe(data.get("zone"))
    contact_type = safe(data.get("contact_type"))
    direction = safe(data.get("direction"))
    quality = safe(data.get("quality"))
    situation = safe(data.get("situation"))
    comment = safe(data.get("comment"))
    batter = safe(data.get("batter"))

    has_data = any(
        [result, pitch, velo, count, zone, contact_type, direction, quality, situation, comment]
    )

    c.setFillColor(SOFT_ORANGE if has_data else colors.white)
    c.setStrokeColor(ORANGE if has_data else GRID)
    c.setLineWidth(1.1 if has_data else 0.7)
    c.roundRect(x, y, w, h, 6, fill=1, stroke=1)

    # AB number
    c.setFillColor(MUTED)
    c.setFont("Helvetica-Bold", 6.5)
    c.drawString(x + 5, y + h - 10, f"AB {ab_num}")

    # Result
    c.setFillColor(result_color(result))
    c.setFont("Helvetica-Bold", 12)
    c.drawString(x + 5, y + h - 24, result if result else "-")

    # Diamond
    draw_diamond(c, x + w - 24, y + h - 31, 17, result)

    # Pitch / velo / zone row
    c.setFillColor(DARK)
    c.setFont("Helvetica-Bold", 6.2)
    c.drawString(x + 5, y + h - 38, f"{pitch} {velo}".strip()[:15])

    c.setFont("Helvetica", 6)
    c.setFillColor(MUTED)
    c.drawString(x + 52, y + h - 38, f"C:{count}"[:10])
    c.drawString(x + 82, y + h - 38, f"Z:{zone}"[:13])

    # Contact line
    c.setFillColor(DARK)
    c.setFont("Helvetica", 6)
    contact = f"{contact_type} -> {direction}".strip(" ->")
    c.drawString(x + 5, y + h - 50, contact[:24])

    c.setFillColor(MUTED)
    c.drawString(x + 5, y + h - 61, quality[:18])

    if batter and batter != "Starter":
        c.setFillColor(ORANGE)
        c.setFont("Helvetica-Bold", 5.7)
        c.drawString(x + 5, y + 20, batter[:26])

    # Comment
    c.setFillColor(DARK)
    c.setFont("Helvetica", 5.6)
    lines = wrap_text(comment, 30)
    start_y = y + 10
    for idx, line in enumerate(lines[:2]):
        c.drawString(x + 5, start_y - idx * 7, line)


def draw_header(c, width, height, game_info):
    c.setFillColor(NAVY)
    c.rect(0, height - 64, width, 64, fill=1, stroke=0)

    draw_logo(c, 22, height - 55, 40, 40)

    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 17)
    c.drawString(74, height - 29, "TIGERS PROFESSIONAL AT-BAT SCOREBOOK")

    c.setFont("Helvetica", 8)
    info = (
        f"Date: {safe(game_info.get('date'))}  |  "
        f"Team: {safe(game_info.get('team'))}  |  "
        f"Opponent: {safe(game_info.get('opponent'))}  |  "
        f"{safe(game_info.get('home_away'))}  |  "
        f"Game #: {safe(game_info.get('game_number'))}  |  "
        f"Inning: {safe(game_info.get('inning'))}  |  "
        f"Score: {safe(game_info.get('score'))}"
    )
    c.drawString(74, height - 47, info[:145])


def draw_player_cell(c, x, y, w, h, idx, player):
    name = safe(player.get("name")) or f"Player {idx + 1}"
    pos = safe(player.get("position"))
    bats = safe(player.get("bats"))

    c.setFillColor(LIGHT)
    c.setStrokeColor(GRID)
    c.setLineWidth(0.8)
    c.roundRect(x, y, w, h, 6, fill=1, stroke=1)

    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 7.2)
    c.drawString(x + 6, y + h - 12, f"{idx + 1}. {name}"[:28])

    c.setFillColor(MUTED)
    c.setFont("Helvetica", 6.2)
    c.drawString(x + 6, y + h - 24, f"POS: {pos}    BATS: {bats}"[:26])

    subs = player.get("subs", [])
    sub_y = y + h - 37
    for sub in subs[:2]:
        sub_name = safe(sub.get("name"))
        if not sub_name:
            continue
        role = safe(sub.get("role"))
        inn = safe(sub.get("inning"))
        sub_pos = safe(sub.get("position"))
        c.setFillColor(ORANGE)
        c.setFont("Helvetica-Bold", 5.8)
        c.drawString(x + 6, sub_y, f"{role}: {sub_name} {sub_pos} Inn {inn}"[:30])
        sub_y -= 8


def draw_page(c, width, height, game_info, lineup, chart_data, ab_start, ab_end):
    draw_header(c, width, height, game_info)

    margin = 18
    top_y = height - 88
    player_w = 132
    available_w = width - (margin * 2) - player_w
    ab_count = ab_end - ab_start + 1
    ab_w = available_w / ab_count

    header_h = 20
    row_h = 54

    # Column headers
    c.setFillColor(ORANGE)
    c.roundRect(margin, top_y, player_w, header_h, 5, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 7.5)
    c.drawCentredString(margin + player_w / 2, top_y + 7, "LINEUP")

    for j, ab in enumerate(range(ab_start, ab_end + 1)):
        x = margin + player_w + j * ab_w
        c.setFillColor(ORANGE)
        c.roundRect(x + 2, top_y, ab_w - 4, header_h, 5, fill=1, stroke=0)
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 7.5)
        c.drawCentredString(x + ab_w / 2, top_y + 7, f"AT-BAT {ab}")

    y = top_y - row_h - 4

    for idx, player in enumerate(lineup[:9]):
        draw_player_cell(c, margin, y, player_w, row_h, idx, player)

        for j, ab in enumerate(range(ab_start, ab_end + 1)):
            x = margin + player_w + j * ab_w
            data = chart_data.get(idx, {}).get(f"ab_{ab}", {})
            draw_ab_box(c, x + 2, y, ab_w - 4, row_h, ab, data)

        y -= row_h + 5

    # Notes footer
    footer_y = 16
    c.setFillColor(LIGHT)
    c.setStrokeColor(GRID)
    c.roundRect(margin, footer_y, width - margin * 2, 32, 6, fill=1, stroke=1)

    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 7)
    c.drawString(margin + 8, footer_y + 20, "GENERAL NOTES")

    c.setFillColor(DARK)
    c.setFont("Helvetica", 6.5)
    notes = wrap_text(safe(game_info.get("notes")), 125)
    for i, line in enumerate(notes[:2]):
        c.drawString(margin + 96, footer_y + 20 - i * 8, line)


def export_chart_pdf(game_info, lineup, chart_data):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=landscape(letter))
    width, height = landscape(letter)

    # Page 1: AB 1-5
    draw_page(c, width, height, game_info, lineup, chart_data, 1, min(5, MAX_ABS))

    # Page 2: AB 6-9 if needed
    if MAX_ABS > 5:
        c.showPage()
        draw_page(c, width, height, game_info, lineup, chart_data, 6, MAX_ABS)

    c.save()
    buffer.seek(0)
    return buffer