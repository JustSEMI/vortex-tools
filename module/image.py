import os
import sys
import subprocess
from rembg import remove, new_session
from PIL import Image, ImageDraw, ImageFont

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
    
def upscale_image(input_path, scale, state_ref):
    state_ref["progress"] = 0.1
    state_ref["status_text"] = "Menyiapkan GPU Vulkan..."
    
    dir_name = os.path.dirname(input_path)
    base_name = os.path.basename(input_path)
    output_path = os.path.join(dir_name, f"upscaled_{base_name}")
    
    upscaler_exe = os.path.join("model", "realesgan-ncnn-vulkan.exe")
    
    cmd = [
        str(upscaler_exe), 
        "-i", str(input_path), 
        "-o", str(output_path), 
        "-s", str(scale), 
        "-n", "realesgan-x4plus"
    ]
    
    try:
        state_ref["progress"] = 0.4
        state_ref["status_text"] = "AI Upscaling sedang berjalan..."
        
        subprocess.run(cmd, check=True, creationflags=subprocess.CREATE_NO_WINDOW)
        
        state_ref["progress"] = 1.0
        state_ref["status_text"] = "Upscale Berhasil!"
        state_ref["is_processing"] = False
        return f"Sukses: {output_path}"
    except Exception as e:
        state_ref["is_processing"] = False
        state_ref["progress"] = 0.0
        return f"Gagal Upscale: {str(e)}"
    
def convert_image(input_path, target_format, state_ref):
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
        return f"Error : {str(e)}"

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