import glfw
import OpenGL.GL as gl
import imgui
import os
import subprocess
import threading
from imgui.integrations.glfw import GlfwRenderer
from tkinter import filedialog, Tk

# --- FFMPEG ---
bin_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bin")
if bin_path not in os.environ["PATH"]:
    os.environ["PATH"] += os.pathsep + bin_path

# --- IMPORT MODULES ---
from module import image, document, audio, downloader, utility

# --- STATE MANAGEMENT ---
state = {
    "selected_file": "Belum ada file dipilih...",
    "selected_doc": "Belum ada dokumen dipilih...",
    "selected_folder": "Pilih folder untuk Batch...",
    "selected_audio": "Belum ada file audio...",
    "wm_text": "Copyright Vortex",
    "wm_opacity": 150,
    "upscale_scale": 4,
    "target_img_format": 0,
    "img_formats": ["JPG", "PNG", "WEBP", "BMP"],
    "target_audio_format": 0,
    "audio_formats": ["MP3", "WAV", "OGG", "FLAC"],
    "target_doc_type": 0,
    "yt_url": "",
    "dl_mode_idx": 0,
    "dl_quality_idx": 0,
    "dl_audio_format_idx": 0,
    "dl_modes": ["Video", "Audio"],
    "dl_qualities": ["Best (4K/2K)", "1080p", "720p"],
    "dl_audio_formats": ["MP3", "WAV", "OGG", "FLAC"],
    "proc_list": [],
    "last_refresh_time": 0,
    "refresh_interval": 10,
    "auto_refresh": False,
    "progress": 0.0,
    "status_text": "Idle",
    "is_processing": False,
    "changelog_text": """VORTEX ULTIMATE - V2 MAJOR UPDATE 07/02/2026
---------------------------
[+] watermark batch processing
[+] document converter (pdf<->docx)
[+] audio converter (mp3, wav, ogg, flac)
[+] social media downloader (yt, ig, tiktok)
[+] improved image upscaler (EDSR)
[+] refined UI theme and layout
[+] RAM manager with process killer
    
Note: Beberapa fitur mungkin memerlukan hak akses administrator.""",
    "log_history": ["[VORTEX] > System Ready",
                    "[VORTEX] > Tools by SEMIII",
                    "[VORTEX] > https://github.com/JustSEMI/vortex-tools"],
}

def log_message(msg):
    state["log_history"].append(f"[VORTEX] > {msg}")
    if len(state["log_history"]) > 12: state["log_history"].pop(0)

def draw_console_log(state):
    imgui.spacing()
    imgui.separator()
    imgui.text("Console Log:")
    imgui.begin_child("logs", 0, 0, border=True)
    for line in state["log_history"]:
        imgui.text(line)
    imgui.end_child()

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
    elif target_type == "audio":
        path = filedialog.askopenfilename(filetypes=[("Audio", "*.mp3;*.wav;*.ogg;*.m4a;*.flac")])
        if path: state["selected_audio"] = path
    root.destroy()

def get_hardware_info():
    try:
        cpu = subprocess.check_output('powershell "(Get-CimInstance Win32_Processor).Name"', shell=True).decode().strip()
        gpu = subprocess.check_output('powershell "(Get-CimInstance Win32_VideoController | Select-Object -First 1).Name"', shell=True).decode().strip()
        return f"CPU: {cpu} | GPU: {gpu}"
    except: return "Hardware: Detected"

def apply_ui_theme():
    style = imgui.get_style()
    style.window_rounding = 0.0
    style.frame_rounding = 6.0
    style.tab_rounding = 8.0
    style.scrollbar_rounding = 8.0
    style.grab_rounding = 6.0
    style.child_rounding = 8.0
    style.colors[imgui.COLOR_WINDOW_BACKGROUND] = (0.1, 0.1, 0.1, 1.0)
    style.colors[imgui.COLOR_CHILD_BACKGROUND] = (0.14, 0.14, 0.14, 1.0)
    style.colors[imgui.COLOR_HEADER] = (0.1, 0.4, 0.6, 1.0)
    style.colors[imgui.COLOR_TAB] = (0.1, 0.1, 0.1, 1.0)
    style.colors[imgui.COLOR_TAB_ACTIVE] = (0.0, 0.47, 0.8, 1.0)
    style.colors[imgui.COLOR_BUTTON] = (0.2, 0.2, 0.2, 1.0)
    style.colors[imgui.COLOR_BUTTON_HOVERED] = (0.26, 0.59, 0.98, 0.8)

def main():
    if not glfw.init(): return
    window = glfw.create_window(900, 600, "Vortex Ultimate - Multi Utility Local", None, None)
    glfw.make_context_current(window)
    imgui.create_context()
    impl = GlfwRenderer(window)
    apply_ui_theme()
    hw_info = get_hardware_info()

    while not glfw.window_should_close(window):
        glfw.poll_events()
        impl.process_inputs()
        imgui.new_frame()

        imgui.set_next_window_size(900, 600)
        imgui.set_next_window_position(0, 0)
        imgui.begin("PrimaryWindow", False, imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_MOVE)

        imgui.text_colored("VORTEX MULTI-TOOL DASHBOARD", 0.0, 0.75, 1.0)
        imgui.text_colored(hw_info, 0.47, 0.47, 0.47)
        imgui.separator()
        imgui.spacing()

        imgui.set_window_font_scale(1.2)

        if imgui.begin_tab_bar("MainTabs"):
            # TAB HOME
            if imgui.begin_tab_item("LOG")[0]:
                imgui.spacing()
                imgui.text_colored("Welcome to Vortex Ultimate", 0.0, 1.0, 0.7)
                imgui.begin_child("LogContent", 0, -25, border=True)
                imgui.push_style_color(imgui.COLOR_TEXT, 0.8, 0.8, 0.8, 1.0)
                imgui.text_wrapped(state["changelog_text"])
                imgui.pop_style_color()
                imgui.end_child()
                imgui.text_disabled("Status: System Stable | Developed by SEMIII")
                imgui.end_tab_item()

            # TAB IMAGE TOOLS
            if imgui.begin_tab_item("IMAGE")[0]:
                imgui.spacing()
                if imgui.button("SELECT IMAGE", 120, 40):
                    threading.Thread(target=lambda: select_path("img")).start()
                imgui.same_line()
                imgui.push_item_width(-1)
                imgui.input_text("##file", os.path.basename(state["selected_file"]), flags=imgui.INPUT_TEXT_READ_ONLY)
                imgui.pop_item_width()

                imgui.spacing()
                if imgui.begin_tab_bar("SubTabs"):
                    if imgui.begin_tab_item("Enhancement")[0]:
                        imgui.spacing()
                        imgui.columns(2, "tools", border=False)
                        # Background Remover
                        imgui.begin_child("bg_remover", 0, 135, border=True)
                        imgui.text_colored("Background Remover", 0.0, 1.0, 0.5)
                        imgui.text_colored("Model:", 0.6, 0.6, 0.6)
                        imgui.spacing()
                        if imgui.button("REMOVE BG", -1, 40):
                            state["is_processing"] = True
                            state["progress"] = 0.0
                            threading.Thread(target=lambda: log_message(image.remove_background(state["selected_file"], state)), daemon=True).start()
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
                            threading.Thread(target=lambda: log_message(image.upscale_image(state["selected_file"], state["upscale_scale"], state)), daemon=True).start()
                        imgui.end_child()
                        imgui.columns(1)
                        draw_console_log(state)
                        imgui.end_tab_item()

                    if imgui.begin_tab_item("Format Converter")[0]:
                        imgui.spacing()
                        imgui.text("Pilih format tujuan:")
                        _, state["target_img_format"] = imgui.combo("Format", state["target_img_format"], state["img_formats"])
                        if imgui.button("START CONVERT", 180, 40):
                            fmt = state["img_formats"][state["target_img_format"]]
                            state["is_processing"] = True
                            state["progress"] = 0.0
                            threading.Thread(target=lambda: log_message(image.convert_image(state["selected_file"], fmt, state)), daemon=True).start()
                        draw_console_log(state)
                        imgui.end_tab_item()

                    if imgui.begin_tab_item("Batch Watermark")[0]:
                        imgui.spacing()
                        if imgui.button("PILIH FOLDER GAMBAR", 180, 40):
                            threading.Thread(target=lambda: select_path("folder")).start()
                        imgui.text(f"Folder: {state['selected_folder']}")
                        _, state["wm_text"] = imgui.input_text("Text WM", state["wm_text"], 50)
                        if imgui.button("PROSES SEMUA FILE", 180, 40):
                            state["is_processing"] = True
                            state["progress"] = 0.0
                            threading.Thread(target=lambda: log_message(image.apply_watermark_batch(state["selected_folder"], state["wm_text"], state)), daemon=True).start()
                        imgui.end_tab_item()
                imgui.end_tab_bar()
                draw_console_log(state)
                imgui.end_tab_item()

            # TAB DOCUMENT
            if imgui.begin_tab_item("DOCUMENT")[0]:
                imgui.spacing()
                if imgui.button("SELECT DOC", 120, 40):
                    threading.Thread(target=lambda: select_path("doc")).start()
                imgui.text(f"File: {os.path.basename(state['selected_doc'])}")
                if imgui.button("CONVERT TO PDF/WORD", 180, 40):
                    log_message("Memulai konversi dokumen...")
                    state["is_processing"] = True
                    state["progress"] = 0.0
                    target = "DOCX" if state["selected_doc"].lower().endswith(".pdf") else "PDF"
                    threading.Thread(target=lambda: log_message(document.convert_doc(state["selected_doc"], target, state)), daemon=True).start()
                draw_console_log(state)
                imgui.end_tab_item()

            # TAB AUDIO
            if imgui.begin_tab_item("AUDIO")[0]:
                imgui.spacing()
                if imgui.button("SELECT AUDIO", 120, 40):
                    threading.Thread(target=lambda: select_path("audio")).start()
                imgui.text(f"File: {os.path.basename(state['selected_audio'])}")
                imgui.spacing()
                _, state["target_audio_format"] = imgui.combo("Target Format", state["target_audio_format"], state["audio_formats"])
                if imgui.button("CONVERT AUDIO", 180, 40):
                    target_fmt = state["audio_formats"][state["target_audio_format"]]
                    state["is_processing"] = True
                    state["progress"] = 0.0
                    threading.Thread(target=lambda: log_message(audio.convert_audio(state["selected_audio"], target_fmt, state)), daemon=True).start()
                draw_console_log(state)
                imgui.end_tab_item()

            # TAB DOWNLOADER
            if imgui.begin_tab_item("DOWNLOADER")[0]:
                imgui.spacing()
                
                imgui.text("Social Media Downloader (YT/IG/TikTok)")
                _, state["yt_url"] = imgui.input_text("URL Link", state["yt_url"], 255)
                
                imgui.columns(2, "dl_settings", border=False)
                _, state["dl_mode_idx"] = imgui.combo("Mode", state["dl_mode_idx"], state["dl_modes"])
                
                imgui.columns(2, "dl_options", border=False)
                if state["dl_modes"][state["dl_mode_idx"]] == "Video":
                    _, state["dl_quality_idx"] = imgui.combo("Quality", state["dl_quality_idx"], state["dl_qualities"])
                else:
                    _, state["dl_audio_format_idx"] = imgui.combo("Audio Format", state["dl_audio_format_idx"], state["dl_audio_formats"])
                
                imgui.columns(1)
                
                imgui.spacing()
                if imgui.button("START DOWNLOAD", 180, 40):
                    url = state["yt_url"]
                    mode = state["dl_modes"][state["dl_mode_idx"]]
                    qual = state["dl_qualities"][state["dl_quality_idx"]]
                    audio_fmt = state["dl_audio_formats"][state["dl_audio_format_idx"]]
                    threading.Thread(target=lambda: log_message(downloader.download_media(url, mode, qual, state, audio_fmt)), daemon=True).start()
                draw_console_log(state)
                imgui.end_tab_item()

            # TAB UTILITY
            if imgui.begin_tab_item("UTILITY")[0]:
                if imgui.begin_tab_bar("UtilitySub"):

                    if imgui.begin_tab_item("RAM Manager")[0]:
                        imgui.spacing()
                        
                        current_time = glfw.get_time()
                        if state["auto_refresh"]:
                            if current_time - state["last_refresh_time"] > state["refresh_interval"]:
                                state["proc_list"] = utility.get_processes()
                                state["last_refresh_time"] = current_time

                        _, state["auto_refresh"] = imgui.checkbox("Auto Refresh", state["auto_refresh"])
                        imgui.same_line()
                        if imgui.button("Refresh Now"):
                            state["proc_list"] = utility.get_processes()
                            state["last_refresh_time"] = current_time
                        
                        imgui.spacing()
                        imgui.columns(3, "proc_table")
                        imgui.text("Name"); imgui.next_column()
                        imgui.text("RAM (MB)"); imgui.next_column()
                        imgui.text("Action"); imgui.next_column()
                        imgui.separator()
                        
                        for p in state.get("proc_list", []):
                            imgui.text(p["name"]); imgui.next_column()
                            imgui.text(f"{p['mem']:.1f}"); imgui.next_column()
                            if imgui.button(f"Kill##{p['pid']}"):
                                log_message(utility.kill_process(p["pid"]))
                                state["proc_list"] = utility.get_processes()
                            imgui.next_column()
                        imgui.columns(1)
                        imgui.end_tab_item()

                    imgui.end_tab_bar()
                imgui.end_tab_item()

            imgui.end_tab_bar()

        if state["is_processing"]:
            imgui.spacing(); imgui.separator(); imgui.spacing()
            imgui.text_colored(state["status_text"], 0.0, 0.8, 1.0) 
            imgui.push_style_color(imgui.COLOR_PLOT_HISTOGRAM, 0.0, 0.9, 0.5, 1.0)
            imgui.progress_bar(state["progress"], (-1, 25), f"{int(state['progress']*100)}%")
            imgui.pop_style_color()
            imgui.spacing()

        # CONSOLE LOG
        #imgui.spacing(); imgui.separator(); imgui.text("Console Log:")
        #imgui.begin_child("logs", 0, 0, border=True)
        #for line in state["log_history"]: imgui.text(line)
        #imgui.end_child()

        imgui.end()
        gl.glClearColor(0.1, 0.1, 0.1, 1.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        imgui.render()
        impl.render(imgui.get_draw_data())
        glfw.swap_buffers(window)

    impl.shutdown()
    glfw.terminate()

if __name__ == "__main__": main()