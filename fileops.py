import shutil
from pathlib import Path

def copy_file(src, dst_folder):
    dst = dst_folder / src.name
    shutil.copy(src, dst)

def find_matching_bmp(int_path, base_folder):
    int_stem = int_path.stem.replace(" ", "").lower()
    bmp_candidates = list(base_folder.glob("*.bmp"))
    matching = [bmp for bmp in bmp_candidates if int_stem in bmp.stem.replace(" ", "").lower()]
    return matching
