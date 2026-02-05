import os
from rembg import remove, new_session
from PIL import Image

session = new_session("u2net")

def remove_background(input_path, state_ref):
    try:
        state_ref["progress"] = 0.1
        state_ref["status_text"] = "Inisialisasi AI..."
        
        base_name = os.path.basename(input_path)
        dir_name = os.path.dirname(input_path)
        output_name = os.path.join(dir_name, f"nobg_{os.path.splitext(base_name)[0]}.png")

        state_ref["progress"] = 0.3
        state_ref["status_text"] = "Menghapus Background (Sabar ya)..."

        with Image.open(input_path) as img:
            output_img = remove(img, session=session)
            state_ref["progress"] = 0.8
            state_ref["status_text"] = "Menyimpan Hasil..."
            output_img.save(output_name)

        state_ref["progress"] = 1.0
        state_ref["status_text"] = "Selesai!"
        state_ref["is_processing"] = False
        return f"Done! Tersimpan: {output_name}"
    except Exception as e:
        state_ref["is_processing"] = False
        state_ref["progress"] = 0.0
        return f"Error: {str(e)}"