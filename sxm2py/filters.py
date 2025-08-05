"""
Lightweight validation routines for binary ``.int`` files.

Benjamin Mallada 2025
"""

import numpy as np
from pathlib import Path


def quick_check_int_file(int_file_path, x_pixels, y_pixels):
    """Validate that an ``.int`` file has data and the expected size."""
    try:
        total_pixels = x_pixels * y_pixels
        expected_bytes = total_pixels * 4  # 4 bytes per float32 value
        if Path(int_file_path).stat().st_size != expected_bytes:
            print(f"Invalid size: {int_file_path.name}")
            return False
        file_data = np.memmap(
            int_file_path, dtype="<f4", mode="r", shape=(total_pixels,)
        )
        return np.any(file_data != 0.0)
    except Exception as error:  # pragma: no cover - printing error
        print(f"Error checking {int_file_path.name}: {error}")
        return False

