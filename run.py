from sxm2py.batch import batch_process_folder

def main():
    batch_process_folder(
        folder_path=r"Q:\USERS\BEN\Scripts\20250512",
        output_subfolder="Processed",
        keywords=["TopoFwd", "It_extFwd"]
    export_images_to_pptx(
        image_folder=r"Q:\USERS\BEN\Scripts\20250512\Processed",
        output_pptx_path=r"Q:\USERS\BEN\Scripts\20250512\STM_Figures.pptx",
        images_per_slide=4
    )
    )

if __name__ == "__main__":
    main()
