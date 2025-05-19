from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.shapes import MSO_AUTO_SHAPE_TYPE
from pathlib import Path
from PIL import Image

def export_images_to_pptx(image_folder, output_pptx_path, images_per_slide=4):
    """
    Exports all .bmp images in a folder into a single .pptx presentation.
    Images are laid out in a grid (e.g. 2x2 or 3x2 per slide).
    """
    image_folder = Path(image_folder)
    bmp_files = sorted(image_folder.glob("*.bmp"))

    if not bmp_files:
        print("No BMP files found.")
        return

    prs = Presentation()
    slide_width = prs.slide_width = Inches(10)
    slide_height = prs.slide_height = Inches(10)

    # Determine layout grid
    layout_map = {
        1: (1, 1),
        2: (1, 2),
        4: (2, 2),
        6: (2, 3),
        9: (3, 3)
    }
    rows, cols = layout_map.get(images_per_slide, (2, 2))
    margin = Inches(0.3)
    row_spacing = Inches(0.1)
    # Space per image
    img_width = (slide_width - (cols + 1) * margin) / cols
    img_height = (slide_height - (rows + 1) * margin) / rows

    slide = None
    for i, bmp in enumerate(bmp_files):
        if i % images_per_slide == 0:
            slide = prs.slides.add_slide(prs.slide_layouts[6])  # blank slide

        row = (i % images_per_slide) // cols
        col = (i % images_per_slide) % cols

        left = margin + col * (img_width + margin)
        top = margin + row * (img_height + margin + row_spacing)
        # Insert image
        try:
            pic = slide.shapes.add_picture(str(bmp), left, top, width=img_width, height=img_height)
            # Adjust vertical position to center image if it becomes shorter

            
        except Exception as e:
            print(f"Could not insert {bmp.name}: {e}")

    prs.save(output_pptx_path)
    print(f"✔ Saved PowerPoint: {output_pptx_path}")
