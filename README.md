# Sistem Pengkoreksi Lembar Jawab (OMR System)
## SDN 2 Pusporenggo

Sistem otomatis untuk mengoreksi lembar jawab siswa dengan akurasi tinggi menggunakan teknologi Computer Vision dan Machine Learning.

## Fitur Utama

- ✅ Deteksi pilihan ganda (A, B, C, D) secara otomatis
- ✅ Membaca 40 soal (20 soal per baris) sesuai template sekolah
- ✅ Koreksi otomatis berdasarkan kunci jawaban
- ✅ Perhitungan skor dan statistik
- ✅ Manajemen database siswa
- ✅ Laporan dan analisis hasil
- ✅ Interface yang user-friendly

## Spesifikasi Lembar Jawab

- **Total Soal:** 40
- **Format:** 2 kolom (soal 1-20, soal 21-40)
- **Pilihan:** A, B, C, D (dalam bentuk kotak)
- **Kertas:** A4
- **Layout:** Soal 1-20 di kolom kiri, Soal 21-40 di kolom kanan

## Teknologi yang Digunakan

- **Python 3.10+** - Bahasa pemrograman utama
- **Streamlit** - Web framework untuk interface
- **OpenCV** - Computer Vision dan image processing
- **NumPy** - Komputasi numerik
- **SQLite** - Database
- **Pillow** - Image processing

## Instalasi

### 1. Clone Repository
```bash
git clone <repository-url>
cd omr-system
```

### 2. Buat Virtual Environment
```bash
# Linux/Mac
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

## Menjalankan Aplikasi

```bash
streamlit run app.py
```

Aplikasi akan membuka di browser: **http://localhost:8501**

## Struktur Project

```
omr-system/
├── app.py                      # Aplikasi utama Streamlit
├── config.py                   # Konfigurasi sistem
├── requirements.txt            # Dependencies
├── README.md                   # Dokumentasi ini
├── .gitignore                  # File yang diabaikan Git
│
├── src/                        # Source code modules
│   ├── __init__.py
│   ├── omr_processor.py        # Engine pemrosesan gambar
│   ├── database.py             # Manajemen database
│   └── utils.py                # Fungsi utility
│
├── data/                       # Data folder (auto-created)
│   ├── students.db             # Database SQLite
│   └── results/                # Folder hasil export
│
├── uploads/                    # Folder untuk upload (auto-created)
├── logs/                       # Folder logs (auto-created)
└── templates/                  # Template lembar jawab
```

## Cara Menggunakan

### 1. Upload Lembar Jawab
- Buka menu **"📸 Koreksi Lembar Jawab"**
- Pilih gambar lembar jawab siswa (JPG/PNG)
- Pastikan gambar jelas dan tidak miring

### 2. Input Kunci Jawaban
- Pilih kunci jawaban dari database
- Atau buat kunci baru di menu **"🔑 Manajemen Kunci Jawaban"**
- Format: 40 karakter (ABCD...)

### 3. Proses Koreksi
- Klik tombol **"🔄 Mulai Koreksi"**
- Sistem otomatis mendeteksi jawaban siswa
- Membandingkan dengan kunci jawaban
- Menampilkan hasil dan skor

### 4. Lihat Hasil
- **Skor** - Jumlah jawaban benar
- **Persentase** - Persentase nilai
- **Grade** - Nilai huruf (A, B, C, D, E)
- **Detail Jawaban** - Jawaban per soal (benar/salah)

### 5. Simpan & Export
- Simpan hasil koreksi ke database
- Lihat statistik di menu **"📊 Laporan & Statistik"**

## Menu Aplikasi

| Menu | Fungsi |
|------|--------|
| **🏠 Beranda** | Panduan singkat dan statistik keseluruhan |
| **📸 Koreksi Lembar Jawab** | Upload dan koreksi otomatis lembar |
| **👥 Manajemen Siswa** | Kelola data siswa |
| **🔑 Manajemen Kunci Jawaban** | Simpan dan manage kunci jawaban |
| **📊 Laporan & Statistik** | Analisis dan laporan hasil koreksi |
| **ℹ️ Bantuan** | Tutorial dan troubleshooting |

## Tips Penggunaan

### 📸 Pengambilan Foto Lembar Jawab

**Pencahayaan:**
- Gunakan cahaya alami atau LED yang merata
- Hindari bayangan di atas lembar
- Jangan gunakan flash langsung

**Posisi Kamera:**
- Posisikan kamera tegak lurus dengan lembar
- Pastikan semua bagian lembar terlihat (terutama bagian jawaban)
- Hindari sudut yang terlalu miring

**Kualitas Gambar:**
- Gunakan resolusi tertinggi (HD atau lebih)
- Fokus pada area jawaban (Section I)
- Ukuran file: maksimal 10MB

### ✏️ Cara Siswa Mengisi
- Isi kotak jawaban dengan rapi dan penuh
- Gunakan pensil atau pulpen yang cukup gelap
- Jangan ada goresan di luar kotak yang dipilih
- Satu soal hanya boleh satu kotak yang diisi

## Troubleshooting

### ❌ Sistem tidak bisa mendeteksi kotak jawaban

**Penyebab:**
- Gambar terlalu blur atau gelap
- Lembar miring atau terpotong
- Template lembar berbeda dengan standar

**Solusi:**
- Ambil foto ulang dengan kualitas lebih baik
- Pastikan pencahayaan merata
- Gunakan template resmi sekolah

### ❌ Hasil koreksi tidak akurat

**Penyebab:**
- Kunci jawaban salah
- Siswa mengisi tidak rapi atau tipis
- Gambar kualitas rendah

**Solusi:**
- Verifikasi kunci jawaban
- Minta siswa mengisi dengan lebih rapi
- Ambil foto ulang

### ❌ Aplikasi crash/error

**Solusi:**
- Refresh halaman browser (F5)
- Gunakan file gambar yang lebih kecil
- Pastikan RAM komputer cukup
- Hubungi administrator

## Penilaian/Grading

Sistem menggunakan skala:

| Grade | Persentase | Keterangan |
|-------|-----------|------------|
| A | 90-100% | Sangat Baik |
| B | 80-89% | Baik |
| C | 70-79% | Cukup |
| D | 60-69% | Kurang |
| E | <60% | Sangat Kurang |

## Database

Sistem menggunakan SQLite dengan tabel:

### Tabel `students`
- `student_id` - ID unik siswa
- `name` - Nama siswa
- `class` - Kelas
- `no_nis` - Nomor induk/NIS
- `created_at` - Tanggal dibuat

### Tabel `answer_keys`
- `key_id` - ID unik kunci
- `name` - Nama kunci jawaban
- `subject` - Mata pelajaran
- `answer_key` - String kunci (ABCD...)
- `total_questions` - Jumlah soal

### Tabel `correction_results`
- `result_id` - ID unik hasil
- `student_id` - Referensi siswa
- `key_id` - Referensi kunci jawaban
- `student_answers` - Jawaban siswa
- `score` - Skor (jumlah benar)
- `percentage` - Persentase nilai
- `grade` - Grade/nilai huruf
- `correction_date` - Tanggal koreksi
- `details` - Detail jawaban per soal (JSON)

## Logging

Sistem mencatat semua aktivitas dalam file `logs/omr_system.log`:
- Loading dan preprocessing gambar
- Deteksi kotak jawaban
- Ekstraksi dan grading
- Operasi database
- Error dan warning

## Performa & Batasan

- **Waktu koreksi:** ~5-10 detik per lembar (tergantung kualitas gambar)
- **Ukuran file gambar:** Maksimal 10MB
- **Resolusi gambar:** Minimal 800x600, Maksimal 4000x4000
- **Akurasi deteksi:** ~95% (tergantung kualitas gambar dan cara pengisian)

## Support & Kontak

Untuk bantuan teknis:
- **Sekolah:** SDN 2 Pusporenggo
- **Alamat:** Ngemplak Rt. 03 Rw. 03 Pusporenggo, Musuk, Boyolali

## Lisensi

Sistem ini dibuat khusus untuk SDN 2 Pusporenggo.

## Versi & Update

- **Versi Saat Ini:** 1.0.0
- **Tanggal Rilis:** 2024
- **Status:** Production Ready

---

**Dibuat dengan ❤️ untuk SDN 2 Pusporenggo**
