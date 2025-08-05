"""
Command-line entry point for batch processing and PowerPoint export.

Benjamin Mallada 2025
"""

from pathlib import Path
from sxm2py.batch import batch_process_folder
from sxm2py.ppt import export_images_to_pptx


def main():
    """Example workflow using the package functions."""
    data_directory = Path("path_to_data")  # TODO: set the correct path

    batch_process_folder(
        data_directory=data_directory,
        output_subfolder_name="Processed",
        keywords=["TopoFwd", "It_extFwd"],
    )

    export_images_to_pptx(
        image_directory=data_directory,
        output_presentation_path=data_directory / "output.pptx",
        images_per_slide=4,
    )


if __name__ == "__main__":
    main()

