import numpy as np
from pathlib import Path

def quick_check_int_file(filename, x_points, y_points):
    try:
        total_pixels = x_points * y_points
        expected_bytes = total_pixels * 4
        if Path(filename).stat().st_size != expected_bytes:
            print(f"Invalid size: {filename.name}")
            return False
        data = np.memmap(filename, dtype='<f4', mode='r', shape=(total_pixels,))
        return np.any(data != 0.0)
    except Exception as e:
        print(f"Error checking {filename.name}: {e}")
        return False
