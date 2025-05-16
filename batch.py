from pathlib import Path
from .processing import process_single_txt_file

def batch_process_folder(folder_path, output_subfolder, keywords):
    folder_path = Path(folder_path)
    output_folder = folder_path / output_subfolder
    output_folder.mkdir(exist_ok=True)

    txt_files = list(folder_path.glob("*.txt"))
    summary = {}

    for txt_file in txt_files:
        kept = process_single_txt_file(txt_file, output_folder, keywords)
        if kept:
            summary[txt_file.name] = kept

    print("\n=== Summary ===")
    for fname, channels in summary.items():
        print(f"{fname}: {len(channels)} channel(s) kept")
        for ch in channels:
            print(f"  - {ch}")

    return summary

