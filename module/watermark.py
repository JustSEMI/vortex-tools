import os
from PIL import Image, ImageDraw, ImageFont

def apply_watermark_grid(input_path, wm_text="Copyright Vortex", opacity=90):
    try:
        if not input_path or not os.path.exists(input_path):
            return "Error: File tidak ditemukan."

        base_img = Image.open(input_path).convert("RGBA")
        txt_layer = Image.new("RGBA", base_img.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(txt_layer)
        
        try:
            font = ImageFont.truetype("arial.ttf", 42)
        except:
            font = ImageFont.load_default()

        width, height = base_img.size
        
        output_dir = os.path.join(os.path.dirname(input_path), "vortex_watermarked")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        for y in range(-50, height, 180): 
            for x in range(-50, width, 250):
                text_overlay = Image.new("RGBA", (400, 200), (0, 0, 0, 0))
                d = ImageDraw.Draw(text_overlay)
                
                # --- TEKNIK HIGH CONTRAST (Outline 4 Sisi) ---
                offset = 1
                shadow_color = (0, 0, 0, opacity)
                text_color = (255, 255, 255, opacity)
                
                d.text((10-offset, 10), wm_text, fill=shadow_color, font=font)
                d.text((10+offset, 10), wm_text, fill=shadow_color, font=font)
                d.text((10, 10-offset), wm_text, fill=shadow_color, font=font)
                d.text((10, 10+offset), wm_text, fill=shadow_color, font=font)
                
                d.text((10, 10), wm_text, fill=text_color, font=font)
                
                rotated_text = text_overlay.rotate(35, expand=1, resample=Image.BICUBIC)
                
                txt_layer.paste(rotated_text, (x, y), rotated_text)

        # Gabungkan layer
        combined = Image.alpha_composite(base_img, txt_layer)
        
        save_path = os.path.join(output_dir, f"wm_vortex_{os.path.basename(input_path)}")
        combined.convert("RGB").save(save_path, "JPEG", quality=95)
        
        return "Berhasil diproses!"

    except Exception as e:
        return f"Error: {str(e)}"

def apply_watermark_batch(folder_path, wm_text, state_ref):
    files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    total = len(files)
    if total == 0: return "Folder Kosong"
    
    state_ref["is_processing"] = True
    for i, f in enumerate(files):
        # Update progress bar
        state_ref["progress"] = (i + 1) / total
        state_ref["status_text"] = f"Processing {i+1}/{total}: {f}"
        
        apply_watermark_grid(os.path.join(folder_path, f), wm_text)
        
    state_ref["status_text"] = "Batch Selesai!"
    state_ref["is_processing"] = False
    return f"Sukses! {total} file tersimpan di folder 'vortex_watermarked'"