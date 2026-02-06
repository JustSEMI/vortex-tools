import os
import shutil
import psutil
import subprocess

def get_processes():
    processes = []
    try:
        if not hasattr(psutil, 'process_iter'):
            return [{"pid": 0, "name": "Conflict: rename your psutil.py", "mem": 0}]
            
        for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
            try:
                mem = proc.info['memory_info'].rss / (1024 * 1024)
                if mem > 10:
                    processes.append({"pid": proc.info['pid'], "name": proc.info['name'], "mem": mem})
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
    except Exception as e:
        return [{"pid": 0, "name": f"Error: {str(e)}", "mem": 0}]
    
    return sorted(processes, key=lambda x: x['mem'], reverse=True)[:20]

def kill_process(pid):
    try:
        if pid == 0: return "Pilih proses yang valid."
        p = psutil.Process(pid)
        p.terminate()
        return f"Berhasil mematikan PID {pid}."
    except Exception as e:
        return f"Gagal: {str(e)}"