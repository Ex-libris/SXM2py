from .io import read_txt_parameters
from .filters import quick_check_int_file
from .fileops import copy_file, find_matching_bmp

def process_single_txt_file(txt_path, output_folder, keywords):
    base_folder = txt_path.parent
    params, channels = read_txt_parameters(txt_path)

    try:
        x_pixels = int(params['xPixel'])
        y_pixels = int(params['yPixel'])
    except KeyError:
        print(f"Skipping {txt_path.name}: missing xPixel or yPixel")
        return []

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

            matching_bmps = find_matching_bmp(int_path, base_folder)
            if matching_bmps:
                copy_file(matching_bmps[0], output_folder)
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
