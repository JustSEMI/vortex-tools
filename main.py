import dearpygui.dearpygui as dpg
import threading
import subprocess
import platform
import os

from module import removebg, upscaler, upscaler

# --- IMPORT MODULES ---
try:
    from module import convertimg
    modules_ready = True
except ImportError as e:
    modules_ready = False
    print(f"Peringatan: Beberapa module belum lengkap: {str(e)}")

dpg.create_context()

state = {"selected_file": ""}

# --- HELPER FUNCTIONS ---
def log_message(msg):
    current_log = dpg.get_value("log_box")
    dpg.set_value("log_box", current_log + f"\n[VORTEX] > {msg}")

def file_selected_callback(sender, app_data):
    file_path = list(app_data['selections'].values())[0]
    state["selected_file"] = file_path
    
    file_name = os.path.basename(file_path)
    if dpg.does_item_exist("img_path_text"):
        dpg.set_value("img_path_text", f"File: {file_name}")
    if dpg.does_item_exist("doc_path_text"):
        dpg.set_value("doc_path_text", f"File: {file_name}")
        
    log_message(f"File berhasil dimuat: {file_name}")

# --- HWINFO ---
def get_hardware_info():
    try:
        cpu_cmd = 'powershell "(Get-CimInstance Win32_Processor).Name"'
        cpu = subprocess.check_output(cpu_cmd, shell=True).decode().strip()
        
        gpu_cmd = 'powershell "(Get-CimInstance Win32_VideoController | Select-Object -First 1).Name"'
        gpu = subprocess.check_output(gpu_cmd, shell=True).decode().strip()
        
        return f"CPU: {cpu} | GPU: {gpu} (Vulkan Mode)"
    except:
        return "Hardware: Detected (Vulkan Ready)"    

# --- WRAPPER FUNCTIONS (Menghubungkan UI ke Modul) ---

def run_remove_bg():
    if not state["selected_file"]:
        log_message("Error: Pilih gambar terlebih dahulu!")
        return
    
    def task():
        log_message("Memproses Background Remover (GPU)...")
        result = removebg.remove_background(state["selected_file"])
        log_message(result)
    
    threading.Thread(target=task, daemon=True).start()

def run_upscale():
    if not state["selected_file"]:
        log_message("Error: Pilih gambar terlebih dahulu!")
        return
    
    scale_val = dpg.get_value("upscale_factor")
    scale = int(scale_val.replace("x", ""))
    
    def task():
        log_message(f"Memproses Upscale {scale}x (GPU)...")
        result = upscaler.upscale_image(state["selected_file"], scale)
        log_message(result)
        
    threading.Thread(target=task, daemon=True).start()

def run_format_convert():
    if not state["selected_file"]:
        log_message("Error: Pilih gambar terlebih dahulu!")
        return
    
    target_fmt = dpg.get_value("combo_img_format")
    
    def task():
        log_message(f"Mengonversi gambar ke {target_fmt}...")
        result = convertimg.convert_image(state["selected_file"], target_fmt)
        log_message(result)
        
    threading.Thread(target=task, daemon=True).start()

# --- UI SETUP ---
with dpg.file_dialog(directory_selector=False, show=False, tag="file_dialog", 
                     width=600, height=400, callback=file_selected_callback):
    dpg.add_file_extension(".*")
    dpg.add_file_extension("Images (*.jpg *.png *.webp){.jpg,.png,.webp}", color=(0, 255, 0, 255))
    dpg.add_file_extension("Docs (*.docx *.pdf){.docx,.pdf}", color=(0, 255, 255, 255))

with dpg.window(label="Vortex Multi-Tools", tag="PrimaryWindow"):
    dpg.add_text("VORTEX MULTI-TOOL DASHBOARD", color=(0, 191, 255))
    dpg.add_text(f"{get_hardware_info()}", color=(120, 120, 120))
    dpg.add_separator()
    dpg.add_spacer(height=10)

    with dpg.tab_bar(tag="MainTabs"):
        
        # --- IMAGE TOOLS ---
        with dpg.tab(label=" IMAGE TOOLS "):
            dpg.add_spacer(height=10)
            with dpg.group(horizontal=True):
                dpg.add_button(label="SELECT IMAGE", width=130, height=30, callback=lambda: dpg.show_item("file_dialog"))
                dpg.add_input_text(default_value="No image selected...", readonly=True, tag="img_path_text", width=-1)
            
            dpg.add_spacer(height=10)
            with dpg.tab_bar():
                with dpg.tab(label="AI Enhancement"):
                    dpg.add_spacer(height=10)
                    with dpg.group(horizontal=True):
                        # Child BG Remover
                        with dpg.child_window(width=280, height=135, border=True):
                            dpg.add_text("Background Remover", color=(0, 255, 127))
                            dpg.add_text("Model: u2net (GPU Support)", color=(150, 150, 150))
                            dpg.add_spacer(height=5)
                            dpg.add_button(label="REMOVE BG", width=-1, height=40, callback=run_remove_bg)
                        
                        # Child Upscaler
                        with dpg.child_window(width=280, height=135, border=True):
                            dpg.add_text("Image Upscaler", color=(0, 255, 127))
                            dpg.add_radio_button(["x2", "x4"], horizontal=True, tag="upscale_factor", default_value="x4")
                            dpg.add_spacer(height=5)
                            dpg.add_button(label="UPSCALE (EDSR)", width=-1, height=40, callback=run_upscale)
                
                with dpg.tab(label="Format Converter"):
                    dpg.add_spacer(height=10)
                    dpg.add_text("Pilih format tujuan:")
                    dpg.add_combo(["JPG", "PNG", "WEBP", "BMP"], tag="combo_img_format", default_value="PNG", width=200)
                    dpg.add_spacer(height=5)
                    dpg.add_button(label="START CONVERT", width=150, height=35, callback=run_format_convert)

        # --- DOCUMENT TOOLS ---
        with dpg.tab(label=" DOCUMENT TOOLS "):
            dpg.add_spacer(height=10)
            with dpg.group(horizontal=True):
                dpg.add_button(label="SELECT DOC", width=130, height=30, callback=lambda: dpg.show_item("file_dialog"))
                dpg.add_input_text(default_value="No doc selected...", readonly=True, tag="doc_path_text", width=-1)
            dpg.add_text("Fungsi dokumen akan segera hadir.", color=(150, 150, 150))

    # FOOTER LOG
    dpg.add_spacer(height=20)
    dpg.add_separator()
    dpg.add_text("Console Log:")
    dpg.add_input_text(tag="log_box", multiline=True, width=-1, height=140, readonly=True)

# THEME & VIEWPORT
with dpg.theme() as global_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (25, 25, 25))
        dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (35, 35, 35))
        dpg.add_theme_color(dpg.mvThemeCol_Button, (50, 50, 50))
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5)

dpg.bind_theme(global_theme)
dpg.create_viewport(title='Vortex Tools - Multi Utility Local', width=750, height=580)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("PrimaryWindow", True)
dpg.start_dearpygui()
dpg.destroy_context()