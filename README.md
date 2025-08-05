# sxm2py

Utility scripts for filtering and packaging scanning tunneling microscopy (STM) data recorded with the Anfatec SXM controller.

The package scans a directory of raw `.int`, `.bmp`, and `.txt` files, removes channels that carry no signal, and collects the useful images and metadata in a new `Processed/` folder. It can also build a PowerPoint presentation from the retained images.

## Features

- Parse `.txt` scan files to discover associated `.int` channels.
- Keep only channels whose `.int` files contain nonzero data.
- Copy matching `.bmp` images and annotate them with a scale bar and scan details.
- Save the results to a `Processed/` folder and print a summary of the channels that were preserved.
- Create a `.pptx` file from the processed images.

## Expected folder structure

```
session/
├── scan1.txt
├── scan1TopoFwd.int
├── scan1TopoFwd.bmp
```

Each `.txt` file holds the channel list and parameters for a scan. The tool reads each file, checks the referenced `.int` files, and keeps only those with meaningful data.

## Installation

```
git clone <repo-url>
cd SXM2py
pip install -e .
```

Required libraries include numpy, Pillow, and python-pptx.

## Usage

```
from pathlib import Path
from sxm2py.batch import batch_process_folder
from sxm2py.ppt import export_images_to_pptx

data_dir = Path("/path/to/data")

batch_process_folder(
    data_directory=data_dir,
    output_subfolder_name="Processed",
    keywords=["TopoFwd", "It_extFwd"],
)

export_images_to_pptx(
    image_directory=data_dir / "Processed",
    output_presentation_path=data_dir / "summary.pptx",
    images_per_slide=4,
)
```

Update `keywords` to match the channel names in your files.
