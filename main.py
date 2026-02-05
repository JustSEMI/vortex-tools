import glfw
import OpenGL.GL as gl
import imgui
import os
import subprocess
import threading
from imgui.integrations.glfw import GlfwRenderer
from tkinter import filedialog, Tk

# --- IMPORT MODULES ---
from module import removebg, upscaler, convertimg, docxtool, watermark

# --- STATE MANAGEMENT ---
state = {
    "selected_file": "Belum ada file dipilih...",
    "selected_doc": "Belum ada dokumen dipilih...",
    "selected_folder": "Pilih folder untuk Batch...",
    "wm_text": "Copyright Vortex",
    "wm_opacity": 150,
    "upscale_scale": 4,
    "target_img_format": 0,
    "img_formats": ["JPG", "PNG", "WEBP", "BMP"],
    "target_doc_type": 0,
    "progress": 0.0,
    "status_text": "Idle",
    "is_processing": False,
    "log_history": ["[VORTEX] > System Ready"]
}

def log_message(msg):
    state["log_history"].append(f"[VORTEX] > {msg}")
    if len(state["log_history"]) > 12: state["log_history"].pop(0)

def select_path(target_type):
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    if target_type == "img":
        path = filedialog.askopenfilename(filetypes=[("Images", "*.jpg;*.png;*.webp;*.bmp")])
        if path: state["selected_file"] = path
    elif target_type == "doc":
        path = filedialog.askopenfilename(filetypes=[("Docs", "*.pdf;*.docx")])
        if path: state["selected_doc"] = path
    elif target_type == "folder":
        path = filedialog.askdirectory()
        if path: state["selected_folder"] = path
    root.destroy()

def get_hardware_info():
    try:
        cpu = subprocess.check_output('powershell "(Get-CimInstance Win32_Processor).Name"', shell=True).decode().strip()
        gpu = subprocess.check_output('powershell "(Get-CimInstance Win32_VideoController | Select-Object -First 1).Name"', shell=True).decode().strip()
        return f"CPU: {cpu} | GPU: {gpu} (Vulkan Mode)"
    except: return "Hardware: Detected (Vulkan Ready)"

def apply_ui_theme():
    style = imgui.get_style()
    style.window_rounding = 0.0
    style.frame_rounding = 4.0
    style.colors[imgui.COLOR_WINDOW_BACKGROUND] = (0.1, 0.1, 0.1, 1.0)
    style.colors[imgui.COLOR_CHILD_BACKGROUND] = (0.14, 0.14, 0.14, 1.0)
    style.colors[imgui.COLOR_HEADER] = (0.1, 0.4, 0.6, 1.0)
    style.colors[imgui.COLOR_TAB] = (0.1, 0.1, 0.1, 1.0)
    style.colors[imgui.COLOR_TAB_ACTIVE] = (0.0, 0.47, 0.8, 1.0)
    style.colors[imgui.COLOR_BUTTON] = (0.2, 0.2, 0.2, 1.0)
    style.colors[imgui.COLOR_BUTTON_HOVERED] = (0.26, 0.59, 0.98, 0.8)

def main():
    if not glfw.init(): return
    window = glfw.create_window(800, 600, "Vortex Tools - Multi Utility Local", None, None)
    glfw.make_context_current(window)
    imgui.create_context()
    impl = GlfwRenderer(window)
    apply_ui_theme()
    hw_info = get_hardware_info()

    while not glfw.window_should_close(window):
        glfw.poll_events()
        impl.process_inputs()
        imgui.new_frame()

        imgui.set_next_window_size(800, 600)
        imgui.set_next_window_position(0, 0)
        imgui.begin("PrimaryWindow", False, imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_MOVE)

        imgui.text_colored("VORTEX MULTI-TOOL DASHBOARD", 0.0, 0.75, 1.0)
        imgui.text_colored(hw_info, 0.47, 0.47, 0.47)
        imgui.separator()
        imgui.spacing()

        if imgui.begin_tab_bar("MainTabs"):
            # TAB IMAGE TOOLS
            if imgui.begin_tab_item("IMAGE TOOLS")[0]:
                imgui.spacing()
                if imgui.button("SELECT IMAGE", 120, 30):
                    threading.Thread(target=lambda: select_path("img")).start()
                imgui.same_line()
                imgui.push_item_width(-1)
                imgui.input_text("##file", os.path.basename(state["selected_file"]), flags=imgui.INPUT_TEXT_READ_ONLY)
                imgui.pop_item_width()

                imgui.spacing()
                if imgui.begin_tab_bar("SubTabs"):
                    if imgui.begin_tab_item("AI Enhancement")[0]:
                        imgui.spacing()
                        imgui.columns(2, "tools", border=False)
                        
                        # Background Remover
                        imgui.begin_child("bg_remover", 0, 135, border=True)
                        imgui.text_colored("Background Remover", 0.0, 1.0, 0.5)
                        imgui.text_colored("Model: u2net (GPU Support)", 0.6, 0.6, 0.6)
                        imgui.spacing()
                        if imgui.button("REMOVE BG", -1, 40):
                            state["is_processing"] = True
                            state["progress"] = 0.0
                            threading.Thread(target=lambda: log_message(removebg.remove_background(state["selected_file"], state)), daemon=True).start()
                        imgui.end_child()
                        
                        imgui.next_column()
                        
                        # Upscaler
                        imgui.begin_child("upscaler", 0, 135, border=True)
                        imgui.text_colored("Image Upscaler", 0.0, 1.0, 0.5)
                        _, state["upscale_scale"] = imgui.slider_int("Scale", state["upscale_scale"], 2, 4)
                        imgui.spacing()
                        if imgui.button("UPSCALE (EDSR)", -1, 40):
                            state["is_processing"] = True
                            state["progress"] = 0.0
                            threading.Thread(target=lambda: log_message(upscaler.upscale_image(state["selected_file"], state["upscale_scale"], state)), daemon=True).start()
                        imgui.end_child()
                        imgui.columns(1)
                        imgui.end_tab_item()

                    if imgui.begin_tab_item("Format Converter")[0]:
                        imgui.spacing()
                        imgui.text("Pilih format tujuan:")
                        _, state["target_img_format"] = imgui.combo("Format", state["target_img_format"], state["img_formats"])
                        if imgui.button("START CONVERT", 150, 35):
                            fmt = state["img_formats"][state["target_img_format"]]
                            state["is_processing"] = True
                            state["progress"] = 0.0
                            threading.Thread(target=lambda: log_message(convertimg.convert_image(state["selected_file"], fmt, state)), daemon=True).start()
                        imgui.end_tab_item()

                    if imgui.begin_tab_item("Batch Watermark")[0]:
                        imgui.spacing()
                        if imgui.button("PILIH FOLDER GAMBAR", 180, 30):
                            threading.Thread(target=lambda: select_path("folder")).start()
                        imgui.text(f"Folder: {state['selected_folder']}")
                        _, state["wm_text"] = imgui.input_text("Text WM", state["wm_text"], 50)
                        if imgui.button("PROSES SEMUA FILE", -1, 40):
                            state["is_processing"] = True
                            state["progress"] = 0.0
                            threading.Thread(target=lambda: log_message(watermark.apply_watermark_batch(state["selected_folder"], state["wm_text"], state)), daemon=True).start()
                        imgui.end_tab_item()
                imgui.end_tab_bar()
                imgui.end_tab_item()

            # TAB DOCUMENT TOOLS
            if imgui.begin_tab_item("DOCUMENT TOOLS")[0]:
                imgui.spacing()
                if imgui.button("SELECT DOC", 120, 30):
                    threading.Thread(target=lambda: select_path("doc")).start()
                imgui.text(f"File: {os.path.basename(state['selected_doc'])}")
                if imgui.button("CONVERT TO PDF/WORD", -1, 40):
                    log_message("Memulai konversi dokumen...")
                    state["is_processing"] = True
                    state["progress"] = 0.0
                    threading.Thread(target=lambda: log_message(docxtool.convert_document(state["selected_doc"], state)), daemon=True).start()
                imgui.end_tab_item()
            imgui.end_tab_bar()

        if state["is_processing"]:
            imgui.spacing()
            imgui.separator()
            imgui.spacing()
    
            imgui.text_colored(state["status_text"], 0.0, 0.8, 1.0) 
    
            imgui.push_style_color(imgui.COLOR_PLOT_HISTOGRAM, 0.0, 0.9, 0.5, 1.0)
            imgui.progress_bar(state["progress"], (-1, 25), f"{int(state['progress']*100)}%")
            imgui.pop_style_color()
    
            imgui.spacing()

        # CONSOLE LOG
        imgui.spacing(); imgui.separator(); imgui.text("Console Log:")
        imgui.begin_child("logs", 0, 0, border=True)
        for line in state["log_history"]: imgui.text(line)
        imgui.end_child()

        imgui.end()
        gl.glClearColor(0.1, 0.1, 0.1, 1.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        imgui.render()
        impl.render(imgui.get_draw_data())
        glfw.swap_buffers(window)

    impl.shutdown(); glfw.terminate()

if __name__ == "__main__": main()