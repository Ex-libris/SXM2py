import shutil
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import matplotlib.pyplot as plt

def copy_file(src, dst_folder):
    dst = dst_folder / src.name
    shutil.copy(src, dst)

def find_matching_bmp(int_path, base_folder):
    int_stem = int_path.stem.replace(" ", "").lower()
    bmp_candidates = list(base_folder.glob("*.bmp"))
    matching = [bmp for bmp in bmp_candidates if int_stem in bmp.stem.replace(" ", "").lower()]
    return matching

def add_scale_bar_to_bmp(bmp_path, scan_range_nm, raw_image_pixel_width, bar_thickness=5):
    """
    Draws a raster scale bar directly onto the .bmp image.
    Keeps appearance simple and publication-friendly.
    """
    try:
        img = Image.open(bmp_path).convert("RGB")
        width, height = img.size
        draw = ImageDraw.Draw(img)

        nm_per_px = scan_range_nm / raw_image_pixel_width
        total_nm = width * nm_per_px

        # Choose reasonable bar length
        bar_lengths_nm = [1000, 500, 200, 100, 50, 25, 20, 10, 5, 2]
        max_bar_nm = total_nm * 0.25
        bar_nm = next((l for l in bar_lengths_nm if l <= max_bar_nm), 10)
        bar_px = int(bar_nm / nm_per_px)

        # Draw scale bar (bottom left)
        x = int(width * 0.05)
        y = int(height * 0.95)

        draw.rectangle([x, y - bar_thickness, x + bar_px, y], fill='white')

        # Add label
        try:
            font = ImageFont.truetype("arial.ttf", size=14)
        except:
            font = ImageFont.load_default()

        draw.text((x, y - bar_thickness - 20), f"{bar_nm} nm", fill='white', font=font)

        img.save(bmp_path)
        print(f"Scale bar added to BMP: {bmp_path.name}")

    except Exception as e:
        print(f"Error drawing scale bar on BMP: {e}")



def render_final_figure_to_fixed_canvas(
    bmp_path,
    scan_range_nm,
    raw_image_pixel_width,
    params,
    canvas_size=(1500, 1500),
    font_size=28
):
    """
    Renders the final annotated BMP to a fixed-size canvas with uniform high-res text.
    Ensures metadata is always readable regardless of image resolution.
    """
    try:
        img = Image.open(bmp_path).convert("RGB")
        img_width, img_height = img.size

        # Create white canvas
        canvas_w, canvas_h = canvas_size
        canvas = Image.new("RGB", (canvas_w, canvas_h), (0, 0, 0))
        draw = ImageDraw.Draw(canvas)

        # Fit image onto canvas, centered
        scale_factor = min((canvas_w * 0.9) / img_width, (canvas_h * 0.9) / img_height)
        new_w = int(img_width * scale_factor)
        new_h = int(img_height * scale_factor)
        img_resized = img.resize((new_w, new_h), Image.BICUBIC)

        x_img = (canvas_w - new_w) // 2
        y_img = (canvas_h - new_h) // 2
        canvas.paste(img_resized, (x_img, y_img))

        # Setup font
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()

        # --- SCALE BAR ---
        nm_per_px = scan_range_nm / raw_image_pixel_width
        total_nm = img_width * nm_per_px
        bar_lengths = [1000, 500, 200, 100, 50, 25, 20, 10,5,2]
        bar_nm = next((b for b in bar_lengths if b <= total_nm * 0.25), 10)

        bar_px = int((bar_nm / nm_per_px) * scale_factor)
        bar_thickness = int(font_size / 2)

        x_bar = x_img + int(new_w * 0.05)
        y_bar = y_img + new_h - int(font_size * 1.5)

        draw.rectangle(
            [x_bar, y_bar - bar_thickness, x_bar + bar_px, y_bar],
            fill='white'
        )

        draw.text(
            (x_bar, y_bar - bar_thickness - font_size - 5),
            f"{bar_nm} nm",
            fill='white',
            font=font
        )

        # --- METADATA ---
        lines = []
        if 'Date' in params and 'Time' in params:
            lines.append(f"{params['Date']} {params['Time']}")
        if 'SetPoint' in params and 'SetPointPhysUnit' in params:
            lines.append(f"I: {params['SetPoint']} {params['SetPointPhysUnit']}")
        if 'Bias' in params and 'BiasPhysUnit' in params:
            lines.append(f"V: {params['Bias']} {params['BiasPhysUnit']}")
        lines.append(f"{bmp_path.stem}")

        padding = 10
        box_w = max(draw.textlength(line, font=font) for line in lines) + 2 * padding
        box_h = len(lines) * (font_size + 6) + 2 * padding
        x_box = canvas_w - box_w - padding
        y_box = canvas_h - box_h - padding

        draw.rectangle([x_box, y_box, x_box + box_w, y_box + box_h], fill=(0, 0, 0, 230))

        for i, line in enumerate(lines):
            draw.text(
                (x_box + padding, y_box + padding + i * (font_size + 6)),
                line,
                fill='white',
                font=font
            )

        canvas.save(bmp_path)
        print(f"✔ Final BMP rendered to fixed canvas: {bmp_path.name}")

    except Exception as e:
        print(f"✘ Error rendering fixed canvas BMP: {e}")