from sxm2py.batch import batch_process_folder

def main():
    batch_process_folder(
        folder_path=path,
        output_subfolder="Processed",
        keywords=["TopoFwd", "It_extFwd"]
    )
    export_images_to_pptx(
        image_folder=path,
        output_pptx_path=path,
        images_per_slide=4
    )

if __name__ == "__main__":
    main()
