import os
from yt_dlp import YoutubeDL

def download_media(url, mode, quality, state, audio_format="mp3"):
    if not url or "http" not in url:
        return "Gagal: Link tidak valid!"

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ffmpeg_path = os.path.join(base_dir, "bin")
    out_folder = os.path.join(base_dir, "downloads")

    if not os.path.exists(out_folder):
        os.makedirs(out_folder)

    ydl_opts = {
        'ffmpeg_location': ffmpeg_path,
        'outtmpl': f'{out_folder}/%(title)s.%(ext)s',
        'quiet': True,
        'no_warnings': True,
    }

    if mode == "Audio Only":
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': audio_format,
                'preferredquality': '192',
            }],
        })
    else:
        if quality == "Best (4K/2K)":
            ydl_opts['format'] = 'bestvideo+bestaudio/best'
        elif quality == "1080p":
            ydl_opts['format'] = 'bestvideo[height<=1080]+bestaudio/best'
        else:
            ydl_opts['format'] = 'bestvideo[height<=720]+bestaudio/best'

    def progress_hook(d):
        if d['status'] == 'downloading':
            p_str = d.get('_percent_str', '0%').replace('%', '').strip()
            try:
                state["progress"] = float(p_str) / 100
                state["status_text"] = f"Downloading: {p_str}%"
            except: pass
        elif d['status'] == 'finished':
            state["status_text"] = "Konversi / Penggabungan..."

    ydl_opts['progress_hooks'] = [progress_hook]

    try:
        state["is_processing"] = True
        state["status_text"] = "Menganalisa URL..."
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        state["is_processing"] = False
        state["progress"] = 1.0
        return f"Berhasil! Tersimpan sebagai {audio_format.upper() if mode == 'Audio Only' else 'Video'}"
    except Exception as e:
        state["is_processing"] = False
        return f"Error: {str(e)}"