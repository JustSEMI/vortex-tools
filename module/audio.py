import os
from pydub import AudioSegment

def convert_audio(input_file, target_format, state):
    if not input_file or "Belum ada" in input_file:
        return "Pilih file audio terlebih dahulu!"
    
    try:
        state["status_text"] = "Membaca Audio..."
        state["progress"] = 0.2
        
        audio = AudioSegment.from_file(input_file)
        
        state["status_text"] = "Proses Konversi..."
        state["progress"] = 0.5
        
        out_name = os.path.splitext(input_file)[0] + f".{target_format.lower()}"
        audio.export(out_name, format=target_format.lower())
        
        state["progress"] = 1.0
        state["is_processing"] = False
        return f"Berhasil! File tersimpan: {os.path.basename(out_name)}"
    except Exception as e:
        state["is_processing"] = False
        return f"Error: {str(e)}"