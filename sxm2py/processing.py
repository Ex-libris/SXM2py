"""
Processing pipeline for single measurement files.

Benjamin Mallada 2025
"""

from .io import read_txt_parameters
from .filters import quick_check_int_file
from .fileops import (
    copy_file,
    find_matching_bmp,
    render_final_figure_to_fixed_canvas,
)


def process_single_txt_file(txt_file_path, output_directory, keywords):
    """Process one ``.txt`` file and copy informative channels."""
    base_directory = txt_file_path.parent
    parameters, channel_filenames = read_txt_parameters(txt_file_path)

    try:
        x_pixels = int(parameters["xPixel"])
        y_pixels = int(parameters["yPixel"])
    except KeyError:
        print(f"Skipping {txt_file_path.name}: missing xPixel or yPixel")
        return []

    # Get physical scan range for scale bar
    scan_range = float(parameters.get("XScanRange", 100.0))  # default fallback

    informative_channels = []

    for channel_filename in channel_filenames:
        if not any(keyword in channel_filename for keyword in keywords):
            continue

        int_file_path = base_directory / channel_filename
        if not int_file_path.exists():
            print(f"Missing .int file: {int_file_path.name}")
            continue

        if quick_check_int_file(int_file_path, x_pixels, y_pixels):
            copy_file(int_file_path, output_directory)
            informative_channels.append(channel_filename)

            # Try to find matching .bmp file and annotate it
            matching_bmp_files = find_matching_bmp(int_file_path, base_directory)
            if matching_bmp_files:
                bmp_file = matching_bmp_files[0]
                copy_file(bmp_file, output_directory)
                copied_bmp_path = output_directory / bmp_file.name
                render_final_figure_to_fixed_canvas(
                    bmp_path=copied_bmp_path,
                    scan_range_nm=scan_range,
                    raw_image_pixel_width=x_pixels,
                    params=parameters,
                )
            else:
                print(
                    f"Warning: No matching BMP found for {int_file_path.name}"
                )
        else:
            print(f"Skipped {channel_filename}: all zeros")

    if informative_channels:
        copy_file(txt_file_path, output_directory)
        print(
            f"{txt_file_path.name} → {len(informative_channels)} channel(s) copied"
        )
    else:
        print(f"{txt_file_path.name} skipped: no informative channels")

    return informative_channels
