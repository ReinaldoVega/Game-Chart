# components/canvas_engine.py

from PIL import Image, ImageDraw
from streamlit_image_coordinates import streamlit_image_coordinates


def create_strike_zone_image(selected_zone=None):
    width, height = 360, 460
    img = Image.new("RGB", (width, height), "#0B1B2E")
    draw = ImageDraw.Draw(img)

    orange = "#FA4616"
    border = "#94A3B8"
    text = "#F8FAFC"
    selected = "#FA4616"
    cell_bg = "#102A44"

    zone_x = 70
    zone_y = 90
    cell_w = 73
    cell_h = 73

    # Chase labels
    draw.text((145, 25), "CHASE UP", fill=border)
    draw.text((28, 235), "IN", fill=border)
    draw.text((295, 235), "AWAY", fill=border)
    draw.text((140, 405), "CHASE DOWN", fill=border)

    # Main 3x3 zone
    zone_number = 1
    for r in range(3):
        for c in range(3):
            x1 = zone_x + c * cell_w
            y1 = zone_y + r * cell_h
            x2 = x1 + cell_w
            y2 = y1 + cell_h

            fill = selected if str(zone_number) == str(selected_zone) else cell_bg
            draw.rectangle([x1, y1, x2, y2], fill=fill, outline=border, width=2)

            draw.text((x1 + 32, y1 + 28), str(zone_number), fill=text)
            zone_number += 1

    # Outer border
    draw.rectangle(
        [zone_x, zone_y, zone_x + cell_w * 3, zone_y + cell_h * 3],
        outline=orange,
        width=4,
    )

    return img


def map_strike_zone_click(x, y):
    zone_x = 70
    zone_y = 90
    cell_w = 73
    cell_h = 73

    # Main zone
    if zone_x <= x <= zone_x + cell_w * 3 and zone_y <= y <= zone_y + cell_h * 3:
        col = int((x - zone_x) // cell_w)
        row = int((y - zone_y) // cell_h)
        return str(row * 3 + col + 1)

    # Chase areas
    if 100 <= x <= 260 and 20 <= y < zone_y:
        return "Chase Up"

    if 100 <= x <= 260 and y > zone_y + cell_h * 3:
        return "Chase Down"

    if x < zone_x and zone_y <= y <= zone_y + cell_h * 3:
        return "Chase In"

    if x > zone_x + cell_w * 3 and zone_y <= y <= zone_y + cell_h * 3:
        return "Chase Away"

    return None


def interactive_strike_zone(selected_zone=None, key="strike_zone"):
    img = create_strike_zone_image(selected_zone)

    click = streamlit_image_coordinates(
        img,
        key=key,
        width=360,
    )

    if click:
        return map_strike_zone_click(click["x"], click["y"])

    return None