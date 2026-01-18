import os
from PIL import Image

def convert_image(input_path, target_format):
    try:
        target_format = target_format.upper()
        pil_format = "JPEG" if target_format == "JPG" else target_format
        
        img = Image.open(input_path)
        
        base_name = os.path.basename(input_path)
        dir_name = os.path.dirname(input_path)
        clean_name = os.path.splitext(base_name)[0]
        
        if pil_format == "JPEG" and img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
            
        output_path = os.path.join(dir_name, f"converted_{clean_name}.{target_format.lower()}")
        
        img.save(output_path, pil_format)
        
        return f"Sukses! Konversi ke {target_format} selesai: {output_path}"
    except Exception as e:
        return f"Error di format_image.py: {str(e)}"