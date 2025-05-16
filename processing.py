from .io import read_txt_parameters
from .filters import quick_check_int_file
import shutil
from .fileops import (
    copy_file, find_matching_bmp, render_final_figure_to_fixed_canvas
)

def process_single_txt_file(txt_path, output_folder, keywords):
    """
    Processes a single .txt file:
    - Copies informative .int channels
    - Copies associated .bmp files
    - Creates a vector-annotated .svg figure from each .bmp
    - Copies the .txt only if any informative channel is found
    """
    base_folder = txt_path.parent
    params, channels = read_txt_parameters(txt_path)

    try:
        x_pixels = int(params['xPixel'])
        y_pixels = int(params['yPixel'])
    except KeyError:
        print(f"Skipping {txt_path.name}: missing xPixel or yPixel")
        return []

    # Get physical scan range for scale bar
    scan_range = float(params.get("XScanRange", 100.0))  # default fallback

    informative_channels = []

    for ch in channels:
        if not any(k in ch for k in keywords):
            continue

        int_path = base_folder / ch
        if not int_path.exists():
            print(f"Missing .int file: {int_path.name}")
            continue

        if quick_check_int_file(int_path, x_pixels, y_pixels):
            copy_file(int_path, output_folder)
            informative_channels.append(ch)

            # Try to find matching .bmp file
            matching_bmps = find_matching_bmp(int_path, base_folder)
            if matching_bmps:
                bmp = matching_bmps[0]
                copied_bmp = output_folder / bmp.name
                copy_file(bmp, output_folder)
                copied_bmp = output_folder / bmp.name
                render_final_figure_to_fixed_canvas(
                    bmp_path=copied_bmp,
                    scan_range_nm=scan_range,
                    raw_image_pixel_width=x_pixels,
                    params=params
                )
            else:
                print(f"Warning: No matching BMP found for {int_path.name}")
        else:
            print(f"Skipped {ch}: all zeros")

    if informative_channels:
        copy_file(txt_path, output_folder)
        print(f"{txt_path.name} → {len(informative_channels)} channel(s) copied")
    else:
        print(f"{txt_path.name} skipped: no informative channels")

    return informative_channels