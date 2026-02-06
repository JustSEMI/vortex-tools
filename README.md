# Vortex Tools - Multi Utility Local

**Sebuah aplikasi Local Multi-Tools berbasis GUI yang dirancang untuk memudahkan pengguna dalam memproses gambar dan dokumen dengan antarmuka yang intuitif dan modern.**

---

## ✨ Fitur Utama

### 1. **IMAGE TOOLS**

#### AI Enhancement
- **Background Remover**
  - Menghapus background gambar secara otomatis menggunakan AI model u2net
  - Didukung oleh GPU dengan akselerasi Vulkan
  - Support format: JPG, PNG, WEBP, BMP
  - Output: Gambar dengan background transparan

- **Image Upscaler**
  - Meningkatkan resolusi gambar hingga 4x lipat menggunakan model EDSR
  - Akselerasi GPU melalui NCNN-Vulkan
  - Pilihan scale: 2x atau 4x
  - Ideal untuk meningkatkan kualitas gambar beresolusi rendah
  - Menggunakan executable RealESRGAN-ncnn-vulkan

#### Format Converter
- Konversi gambar ke berbagai format populer
- Format yang didukung: **JPG**, **PNG**, **WEBP**, **BMP**
- Proses konversi cepat dengan preservasi kualitas tinggi
- UI sederhana dengan dropdown pilihan format

#### Batch Watermark
- Menambahkan watermark teks ke multiple gambar sekaligus
- Pattern grid dengan rotasi 35° untuk perlindungan maksimal
- Text outline untuk kontras tinggi pada berbagai background
- Opacity adjustable (default: 90)
- Hasil tersimpan di folder `vortex_watermarked`
- Progress bar real-time untuk batch processing

### 2. **DOCUMENT TOOLS**
- **PDF to DOCX Converter**
  - Konversi file PDF ke format Microsoft Word (.docx)
  - Preservasi layout dan formatting
  
- **DOCX to PDF Converter**
  - Konversi file Word (.docx) ke format PDF
  - Menggunakan pywin32 untuk konversi native Windows

### 3. AUDIO TOOLS
- **Audio Downloader**
  - Download audio dari video YouTube menggunakan yt-dlp
  - Output dalam format MP3
- **Format Converter**
  - Konversi file audio ke format populer seperti MP3, WAV, AAC menggunakan pydub

---

## 📥 Instalasi

### 1. Clone Repository
```bash
git clone https://github.com/JustSEMI/vortex-tools.git
cd vortex-tools
```
### 2. Install Dependencies For ImGui
```bash
pip install -r imgui glfw PyOpenGL Pillow numpy rembg onnxruntime pdf2docx docx2pdf pywin32 psutil yt-dlp pydub
```
### 3. Install Dependencies For DearPyGui
```bash
pip install dearpygui Pillow numpy rembg onnxruntime pdf2docx docx2pdf pywin32
```
### 4. ImGUI Version
```bash
py main.pyw
```
### 5. DearPyGui Version
```bash
py main_beta.pyw
```

---

## 📁 Struktur Proyek
```bash
vortex-tools/
├── main.pyw
├── main_beta.pyw
├── module/
│   ├── audio.py
│   ├── document.py
│   ├── image.py
│   ├── utility.py
│   └── downloader.py
├── model/
│   bin/
├── README.md
└── LICENSE
```

---

## 🐛 Known Issues & Troubleshooting
- **Masalah Font Watermark**: Jika watermark tidak muncul dengan benar, pastikan font `arial.ttf` tersedia di sistem Anda. Alternatifnya, Anda dapat mengganti font di `module/watermark.py`.
- **Konversi Dokumen Gagal**: Pastikan Microsoft Word terinstal pada sistem Anda untuk fitur konversi DOCX ke PDF dan sebaliknya.
- **Masalah GPU Acceleration**: Pastikan driver GPU Anda sudah diperbarui dan mendukung Vulkan untuk performa optimal pada fitur AI Enhancement.
- **Error Missing DLL**: Jika mengalami error terkait DLL saat menjalankan upscaler, pastikan file `vcomp140.dll` dan `vcomp140d.dll` ada di folder `model/`.
- **Performance Issues**: Untuk performa terbaik, jalankan aplikasi pada sistem dengan spesifikasi memadai, terutama untuk fitur AI yang memanfaatkan GPU.
- **Logging & Debugging**: Periksa log history di bagian bawah aplikasi untuk informasi lebih lanjut tentang proses yang dijalankan dan potensi error.
- **Versi Python**: Aplikasi ini diuji pada Python 3.12.10 (tags/v3.12.10:0cc8128, Apr  8 2025, 12:21:36). Pastikan Anda menggunakan versi yang kompatibel.

## 🤝 Kontribusi
Kontribusi sangat diterima! Silakan fork repository ini dan buat pull request dengan fitur baru, perbaikan bug, atau peningkatan dokumentasi.

## 📄 Lisensi
Proyek ini dilisensikan di bawah MIT License. Lihat file `LICENSE` untuk detail lebih lanjut.

## 🙏 Terima Kasih
Terima kasih telah menggunakan Vortex Tools! Jika Anda menemukan proyek ini bermanfaat, silakan bintang repository ini di GitHub dan bagikan kepada teman-teman Anda.