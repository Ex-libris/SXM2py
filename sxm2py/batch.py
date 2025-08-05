"""
Batch helpers for processing multiple ``.txt`` files.

Benjamin Mallada 2025
"""

from pathlib import Path
from .processing import process_single_txt_file


def batch_process_folder(data_directory, output_subfolder_name, keywords):
    """Process every ``.txt`` file in ``data_directory``."""
    data_directory = Path(data_directory)
    output_folder = data_directory / output_subfolder_name
    output_folder.mkdir(exist_ok=True)

    txt_files = list(data_directory.glob("*.txt"))
    summary = {}

    for txt_file_path in txt_files:
        informative_channels = process_single_txt_file(
            txt_file_path, output_folder, keywords
        )
        if informative_channels:
            summary[txt_file_path.name] = informative_channels

    print("\n=== Summary ===")
    for txt_filename, channel_list in summary.items():
        print(f"{txt_filename}: {len(channel_list)} channel(s) kept")
        for channel_name in channel_list:
            print(f"  - {channel_name}")

    return summary


