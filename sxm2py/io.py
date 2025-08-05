"""
Utilities for parsing parameter ``.txt`` files.

Benjamin Mallada 2025
"""


def parse_value(raw_value):
    """Convert ``raw_value`` to float when possible."""
    try:
        return float(raw_value.replace(",", "."))
    except ValueError:
        return raw_value.strip()


def read_txt_parameters(txt_file_path):
    """Read metadata and channel filenames from a ``.txt`` file."""
    parameters = {}
    channel_filenames = []

    with open(txt_file_path, "r", encoding="utf-8", errors="ignore") as file_handle:
        lines = file_handle.readlines()

    in_file_desc = False
    for line in lines:
        line = line.strip()
        if line.startswith("FileDescBegin"):
            in_file_desc = True
        elif line.startswith("FileDescEnd"):
            in_file_desc = False
        elif in_file_desc and line.startswith("FileName"):
            _, filename = line.split(":", 1)
            channel_filenames.append(filename.strip())
        elif ":" in line:
            try:
                key, value = line.split(":", 1)
                parameters[key.strip()] = parse_value(value.strip())
            except ValueError:
                continue

    return parameters, channel_filenames



