def parse_value(value):
    try:
        return float(value.replace(',', '.'))
    except ValueError:
        return value.strip()

def read_txt_parameters(txt_file):
    """Reads metadata and channel filenames from a .txt file."""
    params = {}
    channels = []

    with open(txt_file, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()

    in_file_desc = False
    for line in lines:
        line = line.strip()
        if line.startswith('FileDescBegin'):
            in_file_desc = True
        elif line.startswith('FileDescEnd'):
            in_file_desc = False
        elif in_file_desc and line.startswith('FileName'):
            _, filename = line.split(':', 1)
            channels.append(filename.strip())
        elif ':' in line:
            try:
                key, value = line.split(':', 1)
                params[key.strip()] = parse_value(value.strip())
            except ValueError:
                continue

    return params, channels


