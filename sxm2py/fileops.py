"""
Utility helpers for copying files and annotating bitmap images.

This module also contains routines to draw scale bars and to render
final figures onto a fixed-size canvas.

Benjamin Mallada 2025
"""

import shutil
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import matplotlib.pyplot as plt

def copy_file(source_file, destination_folder):
    """Copy ``source_file`` into ``destination_folder``."""
    destination_path = destination_folder / source_file.name
    shutil.copy(source_file, destination_path)

def find_matching_bmp(int_file_path, search_directory):
    """Return BMP files whose name resembles that of ``int_file_path``."""
    int_stem = int_file_path.stem.replace(" ", "").lower()
    bmp_candidates = list(search_directory.glob("*.bmp"))
    matching_bmps = [
        bmp_file
        for bmp_file in bmp_candidates
        if int_stem in bmp_file.stem.replace(" ", "").lower()
    ]
    return matching_bmps

def add_scale_bar_to_bmp(
    bmp_path,
    scan_range_nm,
    raw_image_pixel_width,
    bar_thickness=5,
):
    """
    Draw a simple scale bar onto ``bmp_path``.

    The function computes a reasonable bar length based on the scan range
    and writes the information directly on the bitmap.  It is intended to
    keep the image publication friendly.
    """
    try:
        image = Image.open(bmp_path).convert("RGB")
        image_width, image_height = image.size
        drawing_context = ImageDraw.Draw(image)

        nanometers_per_pixel = scan_range_nm / raw_image_pixel_width
        total_scan_nm = image_width * nanometers_per_pixel

        # Choose a reasonable bar length (up to 25% of total scan width)
        bar_length_options = [1000, 500, 200, 100, 50, 25, 20, 10, 5, 2]
        max_bar_length_nm = total_scan_nm * 0.25
        bar_length_nm = next(
            (length for length in bar_length_options if length <= max_bar_length_nm),
            10,
        )
        bar_length_pixels = int(bar_length_nm / nanometers_per_pixel)

        # Draw scale bar in the bottom left corner
        bar_x = int(image_width * 0.05)
        bar_y = int(image_height * 0.95)
        drawing_context.rectangle(
            [bar_x, bar_y - bar_thickness, bar_x + bar_length_pixels, bar_y],
            fill="white",
        )

        # Add numeric label above the bar
        try:
            font = ImageFont.truetype("arial.ttf", size=14)
        except Exception:
            font = ImageFont.load_default()

        drawing_context.text(
            (bar_x, bar_y - bar_thickness - 20),
            f"{bar_length_nm} nm",
            fill="white",
            font=font,
        )

        image.save(bmp_path)
        print(f"Scale bar added to BMP: {bmp_path.name}")

    except Exception as error:  # pragma: no cover - printing error
        print(f"Error drawing scale bar on BMP: {error}")



def render_final_figure_to_fixed_canvas(
    bmp_path,
    scan_range_nm,
    raw_image_pixel_width,
    params,
    canvas_size=(1500, 1500),
    font_size=28,
):
    """
    Renders the final annotated BMP to a fixed-size canvas with uniform high-res text.
    Ensures metadata is always readable regardless of image resolution.
    """
    try:
        image = Image.open(bmp_path).convert("RGB")
        image_width, image_height = image.size

        # Create black canvas where the resized image and metadata will be placed
        canvas_width, canvas_height = canvas_size
        canvas = Image.new("RGB", (canvas_width, canvas_height), (0, 0, 0))
        drawing_context = ImageDraw.Draw(canvas)

        # Fit the image onto the canvas while preserving aspect ratio
        scale_factor = min((canvas_width * 0.9) / image_width, (canvas_height * 0.9) / image_height)
        resized_width = int(image_width * scale_factor)
        resized_height = int(image_height * scale_factor)
        resized_image = image.resize((resized_width, resized_height), Image.BICUBIC)

        image_x = (canvas_width - resized_width) // 2
        image_y = (canvas_height - resized_height) // 2
        canvas.paste(resized_image, (image_x, image_y))

        # Setup font for all annotations
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except Exception:
            font = ImageFont.load_default()

        # --- SCALE BAR ---
        nanometers_per_pixel = scan_range_nm / raw_image_pixel_width
        total_scan_nm = image_width * nanometers_per_pixel
        bar_length_options = [1000, 500, 200, 100, 50, 25, 20, 10, 5, 2]
        bar_length_nm = next(
            (bar for bar in bar_length_options if bar <= total_scan_nm * 0.25),
            10,
        )

        bar_length_pixels = int((bar_length_nm / nanometers_per_pixel) * scale_factor)
        bar_thickness = int(font_size / 2)

        bar_x = image_x + int(resized_width * 0.05)
        bar_y = image_y + resized_height - int(font_size * 1.5)

        drawing_context.rectangle(
            [bar_x, bar_y - bar_thickness, bar_x + bar_length_pixels, bar_y],
            fill="white",
        )

        drawing_context.text(
            (bar_x, bar_y - bar_thickness - font_size - 5),
            f"{bar_length_nm} nm",
            fill="white",
            font=font,
        )

        # --- METADATA ---
        metadata_lines = []
        if "Date" in params and "Time" in params:
            metadata_lines.append(f"{params['Date']} {params['Time']}")
        if "SetPoint" in params and "SetPointPhysUnit" in params:
            metadata_lines.append(
                f"I: {params['SetPoint']} {params['SetPointPhysUnit']}"
            )
        if "Bias" in params and "BiasPhysUnit" in params:
            metadata_lines.append(
                f"V: {params['Bias']} {params['BiasPhysUnit']}"
            )
        metadata_lines.append(f"{bmp_path.stem}")

        padding = 10
        box_width = max(drawing_context.textlength(line, font=font) for line in metadata_lines) + 2 * padding
        box_height = len(metadata_lines) * (font_size + 6) + 2 * padding
        box_x = canvas_width - box_width - padding
        box_y = canvas_height - box_height - padding

        drawing_context.rectangle(
            [box_x, box_y, box_x + box_width, box_y + box_height],
            fill=(0, 0, 0, 230),
        )

        for index, line in enumerate(metadata_lines):
            drawing_context.text(
                (box_x + padding, box_y + padding + index * (font_size + 6)),
                line,
                fill="white",
                font=font,
            )

        canvas.save(bmp_path)
        print(f"✔ Final BMP rendered to fixed canvas: {bmp_path.name}")

    except Exception as error:  # pragma: no cover - printing error
        print(f"✘ Error rendering fixed canvas BMP: {error}")
