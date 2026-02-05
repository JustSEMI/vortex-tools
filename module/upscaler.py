import os
import sys
import subprocess

def upscale_image(input_path, scale, state_ref):
    state_ref["progress"] = 0.1
    state_ref["status_text"] = "Menyiapkan GPU Vulkan..."
    
    dir_name = os.path.dirname(input_path)
    base_name = os.path.basename(input_path)
    output_path = os.path.join(dir_name, f"upscaled_{base_name}")
    
    # Path ke exe upscaler
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
        
        # Jalankan proses
        subprocess.run(cmd, check=True, creationflags=subprocess.CREATE_NO_WINDOW)
        
        state_ref["progress"] = 1.0
        state_ref["status_text"] = "Upscale Berhasil!"
        state_ref["is_processing"] = False
        return f"Sukses: {output_path}"
    except Exception as e:
        state_ref["is_processing"] = False
        state_ref["progress"] = 0.0
        return f"Gagal Upscale: {str(e)}"