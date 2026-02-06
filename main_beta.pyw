import dearpygui.dearpygui as dpg
import os
import threading
import subprocess
from tkinter import filedialog, Tk

# --- IMPORT MODULES ---
from module import image, document, sound

# --- HARDWARE INFO ---
def get_hardware_info():
    try:
        cpu = subprocess.check_output('powershell "(Get-CimInstance Win32_Processor).Name"', shell=True).decode().strip()
        try:
            gpu = subprocess.check_output('powershell "(Get-CimInstance Win32_VideoController | Select-Object -First 1).Name"', shell=True).decode().strip()
        except:
            gpu = "Integrated Graphics"
        return f"CPU: {cpu} | GPU: {gpu} (Vulkan Mode)"
    except:
        return "Hardware: Detected (Vulkan Ready)"

# --- LOGIC HELPERS ---
def log_message(msg):
    current_logs = dpg.get_value("console_log")
    log_lines = current_logs.split('\n')
    if len(log_lines) > 12: 
        log_lines.pop(0)
    new_log = "\n".join(log_lines) + f"\n[VORTEX] > {msg}"
    dpg.set_value("console_log", new_log.strip())
    dpg.set_y_scroll("log_child", 1.0)

def select_path(target):
    root = Tk(); root.withdraw(); root.attributes('-topmost', True)
    if target == "img":
        path = filedialog.askopenfilename(filetypes=[("Images", "*.jpg;*.png;*.webp;*.bmp")])
        if path: 
            dpg.set_value("path_img_text", os.path.basename(path))
            state["img"] = path
    elif target == "doc":
        path = filedialog.askopenfilename(filetypes=[("Docs", "*.pdf;*.docx")])
        if path: 
            dpg.set_value("path_doc_text", os.path.basename(path))
            state["doc"] = path
    elif target == "folder":
        path = filedialog.askdirectory()
        if path: 
            dpg.set_value("path_folder_text", path)
            state["folder"] = path
    root.destroy()

# --- STATE MANAGEMENT ---
state = {"img": "", "doc": "", "folder": "", "progress": 0.0}

class StateRef:
    def __getitem__(self, key): return state.get(key)
    def __setitem__(self, key, value):
        state[key] = value
        if key == "progress": dpg.set_value("progress_bar", value)
        if key == "status_text": dpg.set_value("status_text", value)

state_ref = StateRef()

# --- GUI SETUP ---
dpg.create_context()
dpg.create_viewport(title='Vortex Tools - Multi Utility Local', width=800, height=650)

with dpg.window(label="Main", tag="PrimaryWindow"):
    dpg.add_text("VORTEX MULTI-TOOL DASHBOARD", color=[0, 191, 255]) 
    dpg.add_text(get_hardware_info(), color=[120, 120, 120],)
    dpg.add_separator()
    dpg.add_spacer(height=5)

    with dpg.tab_bar():
        # --- IMAGE TOOLS ---
        with dpg.tab(label=" IMAGE TOOLS "):
            dpg.add_spacer(height=5)
            with dpg.group(horizontal=True):
                dpg.add_button(label="SELECT IMAGE", width=120, height=25, callback=lambda: threading.Thread(target=lambda: select_path("img")).start())
                dpg.add_input_text(tag="path_img_text", default_value="Belum ada file dipilih...", readonly=True, width=-1)
            
            dpg.add_spacer(height=10)

            with dpg.tab_bar():
                with dpg.tab(label="AI Enhancement"):
                    dpg.add_spacer(height=5)
                    with dpg.table(header_row=False, borders_innerH=False, borders_innerV=False, borders_outerH=False, borders_outerV=False):
                        dpg.add_table_column()
                        dpg.add_table_column()
                        
                        with dpg.table_row():
                            with dpg.child_window(height=150, border=True):
                                dpg.add_text("Background Remover", color=[0, 255, 128])
                                dpg.add_text("Model: u2net (GPU Support)", color=[150, 150, 150])
                                dpg.add_spacer(height=10)
                                dpg.add_button(label="REMOVE BG", width=-1, height=40,
                                    callback=lambda: threading.Thread(target=lambda: log_message(image.remove_background(state["img"], state_ref)), daemon=True).start())

                            with dpg.child_window(height=150, border=True):
                                dpg.add_text("Image Upscaler", color=[0, 255, 128])
                                dpg.add_slider_int(label="Scale", default_value=4, min_value=2, max_value=4, width=-100)
                                dpg.add_spacer(height=10)
                                dpg.add_button(label="UPSCALE (EDSR)", width=-1, height=40,
                                    callback=lambda: threading.Thread(target=lambda: log_message(image.upscale_image(state["img"], 4, state_ref)), daemon=True).start())

                with dpg.tab(label="Format Converter"):
                    dpg.add_spacer(height=10)
                    dpg.add_text("Pilih format tujuan:")
                    combo_fmt = dpg.add_combo(["JPG", "PNG", "WEBP", "BMP"], default_value="PNG", width=200)
                    dpg.add_spacer(height=5)
                    dpg.add_button(label="START CONVERT", width=200, height=35,
                        callback=lambda: threading.Thread(target=lambda: log_message(image.convert_image(state["img"], dpg.get_value(combo_fmt), state_ref)), daemon=True).start())

                with dpg.tab(label="Batch Watermark"):
                    dpg.add_spacer(height=10)
                    dpg.add_button(label="PILIH FOLDER GAMBAR", width=200, height=30, callback=lambda: threading.Thread(target=lambda: select_path("folder")).start())
                    dpg.add_text("Folder: ...", tag="path_folder_text")
                    wm_in = dpg.add_input_text(label="Text WM", default_value="Copyright Vortex", width=300)
                    dpg.add_spacer(height=5)
                    dpg.add_button(label="PROSES SEMUA FILE", width=-1, height=40,
                        callback=lambda: threading.Thread(target=lambda: log_message(image.apply_watermark_batch(state["folder"], dpg.get_value(wm_in), state_ref)), daemon=True).start())

        # --- DOCUMENT TOOLS ---
        with dpg.tab(label=" DOCUMENT TOOLS "):
            dpg.add_spacer(height=10)
            dpg.add_button(label="SELECT DOC", width=120, height=30, callback=lambda: threading.Thread(target=lambda: select_path("doc")).start())
            dpg.add_text("File: ...", tag="path_doc_text")
            dpg.add_spacer(height=10)
            dpg.add_button(label="CONVERT TO PDF/WORD", width=-1, height=40,
                 callback=lambda: threading.Thread(target=lambda: log_message(document.convert_doc(state["doc"], "DOCX" if str(state["doc"]).lower().endswith(".pdf") else "PDF", state_ref)), daemon=True).start())

    dpg.add_spacer(height=10)
    dpg.add_separator()
    dpg.add_spacer(height=5)
    dpg.add_text("Idle", tag="status_text", color=[0, 200, 255])
    
    with dpg.theme() as pbar_theme:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_PlotHistogram, [0, 230, 118])
    
    pb = dpg.add_progress_bar(tag="progress_bar", default_value=0.0, width=-1, height=20)
    dpg.bind_item_theme(pb, pbar_theme)

    # CONSOLE LOG AREA
    dpg.add_spacer(height=10)
    dpg.add_separator()
    dpg.add_text("Console Log:")
    with dpg.child_window(tag="log_child", height=150, border=True):
        dpg.add_text("[VORTEX] > System Ready", tag="console_log")

# --- THEME SETUP ---
with dpg.theme() as global_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 0)
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 4)
        dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, 4)
        
        dpg.add_theme_color(dpg.mvThemeCol_WindowBg, [26, 26, 26])
        dpg.add_theme_color(dpg.mvThemeCol_ChildBg, [36, 36, 36])
        dpg.add_theme_color(dpg.mvThemeCol_Header, [26, 102, 153])
        dpg.add_theme_color(dpg.mvThemeCol_Tab, [26, 26, 26])
        dpg.add_theme_color(dpg.mvThemeCol_TabHovered, [26, 102, 153])
        dpg.add_theme_color(dpg.mvThemeCol_TabActive, [0, 120, 215])
        dpg.add_theme_color(dpg.mvThemeCol_Button, [51, 51, 51])
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, [66, 150, 250])
        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, [0, 120, 215])

dpg.bind_theme(global_theme)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("PrimaryWindow", True)
dpg.start_dearpygui()
dpg.destroy_context()