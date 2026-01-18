# Vortex Tools - Multi Utility Local

**Sebuah aplikasi Local Multi-Tools yang dirancang untuk memudahkan pengguna dalam mengelola dan memproses gambar serta dokumen dengan antarmuka grafis yang intuitif.**

---

## 📋 Daftar Isi
- [Fitur Utama](#fitur-utama)
- [Persyaratan Sistem](#persyaratan-sistem)
- [Instalasi](#instalasi)
- [Penggunaan](#penggunaan)
- [Struktur Proyek](#struktur-proyek)
- [Teknologi](#teknologi)

---

## ✨ Fitur Utama

### 1. **IMAGE TOOLS**

#### AI Enhancement
- **Background Remover**
  - Menghapus background gambar secara otomatis menggunakan model u2net
  - Didukung oleh GPU (Vulkan Mode) untuk performa optimal
  - Input: Gambar (JPG, PNG, WEBP)
  - Output: Gambar tanpa background

- **Image Upscaler**
  - Meningkatkan resolusi gambar hingga 4x lipat
  - Menggunakan model EDSR dengan akselerasi GPU
  - Opsi: 2x atau 4x upscaling
  - Ideal untuk meningkatkan kualitas gambar beresolusi rendah

#### Format Converter
- Konversi gambar ke berbagai format
- Format yang didukung: **JPG**, **PNG**, **WEBP**, **BMP**
- Proses konversi yang cepat dan efisien

### 2. **DOCUMENT TOOLS**
- Fitur dokumen sedang dalam pengembangan (coming soon)
- Rencananya akan mendukung file: `.docx`, `.pdf`

---

## 🖥️ Persyaratan Sistem

### Hardware
- **GPU yang mendukung Vulkan** (untuk akselerasi GPU)
- **RAM**: Minimal 4GB (direkomendasikan 8GB ke atas)
- **Storage**: Minimal 2GB ruang bebas

### Software
- **OS**: Windows 7 atau lebih baru
- **Python**: 3.8 atau lebih tinggi
- **Dependencies**: Lihat file `requirements.txt`

---

## 📥 Instalasi

### 1. Clone Repository
```bash
git clone https://github.com/JustSEMI/vortex-tools.git
cd vortex-tools
```

### 2. Instalasi Dependencies
```bash
pip install -r requirements.txt
```

### 3. Jalankan Aplikasi
```bash
python main.py
```

---

## 🚀 Penggunaan

### Menggunakan Background Remover
1. Buka aplikasi **Vortex Multi-Tools**
2. Masuk ke tab **IMAGE TOOLS**
3. Klik **SELECT IMAGE** dan pilih gambar Anda
4. Pergi ke tab **AI Enhancement**
5. Klik tombol **REMOVE BG**
6. Tunggu proses selesai (hasil akan ditampilkan di log)

### Menggunakan Image Upscaler
1. Pilih gambar yang ingin di-upscale
2. Di tab **AI Enhancement**, pilih faktor upscaling (2x atau 4x)
3. Klik **UPSCALE (EDSR)**
4. Tunggu proses selesai

### Menggunakan Format Converter
1. Pilih gambar yang ingin dikonversi
2. Masuk ke tab **Format Converter**
3. Pilih format target (JPG, PNG, WEBP, atau BMP)
4. Klik **START CONVERT**
5. File hasil konversi akan disimpan di lokasi yang sama

---

## 📁 Struktur Proyek

```
vortex-tools/
├── main.py                 # File utama aplikasi (UI & logic)
├── README.md              # Dokumentasi proyek
├── requirements.txt       # Dependencies Python
├── module/
│   ├── __init__.py        # Module initialization
│   ├── removebg.py        # Module Background Remover
│   ├── upscaler.py        # Module Image Upscaler
│   ├── convertimg.py      # Module Format Converter
│   └── __pycache__/       # Cache Python
└── model/                 # Model AI dan weights
    └── (model files)
```

---

## 🛠️ Teknologi

### Libraries Utama
- **DearPyGui** - Framework GUI untuk antarmuka grafis
- **Python 3.x** - Bahasa pemrograman utama
- **GPU Acceleration** - Vulkan Mode untuk performa maksimal

### Model AI
- **u2net** - Untuk Background Removal
- **EDSR** - Untuk Image Upscaling

### Processing
- **Threading** - Untuk proses non-blocking
- **Subprocess** - Untuk pengambilan hardware info
- **GPU Support** - Akselerasi melalui Vulkan

---

## 📝 Catatan

- Pastikan GPU Anda mendukung Vulkan untuk performa optimal
- Semua proses berjalan secara asynchronous (tidak membuat UI hang)
- Log konsol menampilkan status setiap operasi
- Hasil output disimpan di folder yang sama dengan file input

---

## 📄 Lisensi

Proyek ini adalah open-source dan dapat digunakan secara bebas.

---

## 👤 Kontribusi

Untuk berkontribusi, silakan:
1. Fork repository ini
2. Buat branch fitur baru
3. Commit perubahan Anda
4. Push ke branch
5. Buat Pull Request

---

**Dikembangkan oleh JustSEMI** | Vortex Tools v1.0
