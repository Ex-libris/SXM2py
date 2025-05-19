# sxm2py

**STM Channel Filter and Extractor for Anfatec SXM Controller Data**

`sxm2py` is a Python tool to batch-process STM data acquired using the Anfatec SXM controller. It filters `.int` channel files based on signal content, preserving only those that contain non-zero data. It also copies matching `.bmp` image files and associated `.txt` metadata files for further analysis into a different subfolder 'Processed'.

---

## Features

- Reads `.txt` metadata files listing channels from the SXM controller
- Filters `.int` binary data files, keeping only those with actual signal (not all zeros). At the moment is focused in topography and current channels.
- Copies corresponding `.bmp` images (matched by filename stem) into a subfolder.
- Skips empty channels or missing files
- Outputs a flat folder (`Processed/`) with cleaned data


## Expected Input Folder Structure

Folder \
├── scan1.txt \
├── scan1TopoFwd.int \
├── scan1TopoFwd.bmp 

Each `.txt` file describes the scan parameters and lists the `.int` files used. This tool will parse each `.txt`, inspect the listed `.int` files, and retain only those that contain real data. This is for example useful to avoid bacward/forward empty files, channels that are preserved but contain no changes (Bias, qPlus AFM is there is no afm acquisition, LIAX, LIAY, etc)

## How to Use

You must run the file 'run.py'. In path of batch_process_folder put your path to your datafiles. By default I have kept onlt the topgrahy forward channel and the tunneling current, but you can add any other names tfor matching your file names :
from sxm2py.batch import batch_process_folder

batch_process_folder(
    folder_path=path,
    output_subfolder="Processed",
    keywords=["TopoFwd", "It_extFwd"]
)
