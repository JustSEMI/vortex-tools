import os
from rembg import remove, new_session
from PIL import Image

session = new_session("u2net")

def remove_background(input_path):
    try:
        base_name = os.path.basename(input_path)
        dir_name = os.path.dirname(input_path)
        output_name = os.path.join(dir_name, f"nobg_{os.path.splitext(base_name)[0]}.png")

        with Image.open(input_path) as img:
            output_img = remove(img, session=session)
            output_img.save(output_name)

        return f"Done! Background telah dihapus: {output_name}"
    except Exception as e:
        return f"Error pada module removebg.py: {str(e)}"