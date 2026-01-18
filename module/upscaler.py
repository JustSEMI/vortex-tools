import subprocess
import os

def upscale_image(input_path, output_path, scale=4):
    # Sesuaikan dengan struktur folder di VS Code kamu
    # Folder 'model' ada di root proyek
    base_dir = os.path.dirname(os.path.dirname(__file__))
    upscaler_path = os.path.join(base_dir, "model", "realesgan-ncnn-vulkan.exe")
    
    # Pastikan scale diubah menjadi string karena subprocess tidak mau menerima int
    cmd = [
        str(upscaler_path), 
        "-i", str(input_path), 
        "-o", str(output_path), 
        "-s", str(scale), 
        "-n", "realesgan-x4plus"
    ]
    
    try:
        # Menjalankan proses vulkan
        subprocess.run(cmd, check=True, creationflags=subprocess.CREATE_NO_WINDOW)
        return True
    except Exception as e:
        print(f"Error Vulkan: {e}")
        return False