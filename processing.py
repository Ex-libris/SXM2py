from .io import read_txt_parameters
from .filters import quick_check_int_file
from .fileops import copy_file, find_matching_bmp
import shutil
def process_single_txt_file(txt_path, output_folder, keywords):
    """
    Processes a single .txt file:
    - Copies informative .int channels
    - Copies associated .bmp files
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

    informative_channels = []

    for ch in channels:
        if not any(k in ch for k in keywords):
            continue

        int_path = base_folder / ch
        if not int_path.exists():
            print(f"Missing .int file: {int_path.name}")
            continue

        if quick_check_int_file(int_path, x_pixels, y_pixels):
            # Copy the .int file
            shutil.copy(int_path, output_folder / int_path.name)
            informative_channels.append(ch)

            # Copy the .bmp file with same name but .bmp extension
            # Try to find a .bmp file in the folder with the .int stem as substring
            bmp_candidates = list(base_folder.glob("*.bmp"))
            int_stem = int_path.stem.replace(" ", "").lower()

            # Try loose matching: remove spaces, compare lowercase
            matching_bmps = [
                bmp for bmp in bmp_candidates
                if int_stem in bmp.stem.replace(" ", "").lower()
            ]

            if len(matching_bmps) == 1:
                shutil.copy(matching_bmps[0], output_folder / matching_bmps[0].name)
            elif len(matching_bmps) > 1:
                print(f"Multiple BMP matches for {int_path.name}; copying first: {matching_bmps[0].name}")
                shutil.copy(matching_bmps[0], output_folder / matching_bmps[0].name)
            else:
                print(f"Warning: No matching BMP found for {int_path.name}")

        else:
            print(f"Skipped {ch}: flat or uniform")

    if informative_channels:
        shutil.copy(txt_path, output_folder / txt_path.name)
        print(f"{txt_path.name} → {len(informative_channels)} channel(s) copied")

    else:
        print(f"{txt_path.name} skipped: no informative channels")

    return informative_channels

