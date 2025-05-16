from sxm2py.batch import batch_process_folder

def main():
    batch_process_folder(
        folder_path=path,
        output_subfolder="Processed",
        keywords=["TopoFwd", "It_extFwd"]
    )

if __name__ == "__main__":
    main()
