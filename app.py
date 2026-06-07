"""
Aplikasi Streamlit untuk Sistem Pengkoreksi Lembar Jawab
SDN 2 Pusporenggo
"""

import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io
import os
from datetime import datetime

import config
from src.omr_processor import OMRProcessor
from src.database import OMRDatabase
from src import utils

# ===== KONFIGURASI STREAMLIT =====
st.set_page_config(
    page_title="Sistem Pengkoreksi Lembar Jawab",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .header-text {
        text-align: center;
        color: #2c3e50;
        margin-bottom: 10px;
    }
    .subheader-text {
        text-align: center;
        color: #7f8c8d;
        font-size: 14px;
        margin-bottom: 20px;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 15px;
        margin: 10px 0;
    }
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 5px;
        padding: 15px;
        margin: 10px 0;
    }
    .info-box {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        border-radius: 5px;
        padding: 15px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# ===== INISIALISASI SESSION STATE =====
if 'processor' not in st.session_state:
    st.session_state.processor = OMRProcessor()

if 'database' not in st.session_state:
    st.session_state.database = OMRDatabase()

if 'current_result' not in st.session_state:
    st.session_state.current_result = None

# Create directories
utils.create_directories()

# ===== HEADER =====
st.markdown("""
<div class="header-text">
    <h1>📋 SISTEM PENGKOREKSI LEMBAR JAWAB</h1>
</div>
<div class="subheader-text">
    <p><strong>SEKOLAH DASAR NEGERI 2 PUSPORENGGO</strong></p>
    <p>Ngemplak Rt. 03 Rw. 03 Pusporenggo, Musuk, Boyolali</p>
</div>
""", unsafe_allow_html=True)

st.divider()

# ===== SIDEBAR =====
with st.sidebar:
    st.header("⚙️ Menu Utama")
    
    menu = st.radio(
        "Pilih Menu:",
        [
            "🏠 Beranda",
            "📸 Koreksi Lembar Jawab",
            "👥 Manajemen Siswa",
            "🔑 Manajemen Kunci Jawaban",
            "📊 Laporan & Statistik",
            "ℹ️ Bantuan"
        ]
    )
    
    st.divider()
    
    # Info sistem
    st.subheader("ℹ️ Informasi Sistem")
    st.info(f"""
    **Spesifikasi:**
    - Total Soal: {config.TOTAL_QUESTIONS}
    - Pilihan: {', '.join(config.CHOICES).upper()}
    - Format: 2 Kolom
    - Soal/Kolom: {config.QUESTIONS_PER_ROW}
    """)

# ===== HALAMAN UTAMA: BERANDA =====
if menu == "🏠 Beranda":
    st.header("Selamat Datang!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📌 Panduan Penggunaan")
        st.markdown("""
        1. **Siapkan Lembar Jawab**
           - Pastikan lembar jelas dan tidak miring
           - Gunakan template resmi sekolah
           
        2. **Ambil Foto/Scan**
           - Format: JPG, PNG
           - Resolusi: Minimal 800x600
           
        3. **Koreksi Otomatis**
           - Upload gambar ke menu "Koreksi"
           - Pilih kunci jawaban
           - Sistem otomatis mendeteksi jawaban
           
        4. **Lihat Hasil**
           - Skor dan persentase
           - Detail jawaban siswa
           - Export ke Excel
        """)
    
    with col2:
        st.subheader("⚡ Fitur Utama")
        st.markdown("""
        ✅ Deteksi otomatis pilihan ganda
        ✅ Koreksi akurat & cepat
        ✅ Manajemen database siswa
        ✅ Laporan statistik lengkap
        ✅ Export hasil ke Excel
        ✅ Mudah digunakan (user-friendly)
        """)
    
    st.divider()
    
    st.subheader("📊 Statistik Sistem")
    stats = st.session_state.database.get_statistics_summary()
    
    if stats and stats['total_corrections']:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Siswa", stats['total_students'] or 0)
        with col2:
            st.metric("Total Koreksi", stats['total_corrections'] or 0)
        with col3:
            avg_pct = stats['avg_percentage'] or 0
            st.metric("Rata-rata Nilai", f"{avg_pct:.1f}%")
        with col4:
            max_pct = stats['max_percentage'] or 0
            st.metric("Nilai Tertinggi", f"{max_pct:.1f}%")
    else:
        st.info("📭 Belum ada data koreksi")

# ===== HALAMAN: KOREKSI LEMBAR JAWAB =====
elif menu == "📸 Koreksi Lembar Jawab":
    st.header("📸 Koreksi Lembar Jawab Siswa")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("1. Upload Lembar Jawab")
        uploaded_file = st.file_uploader(
            "Pilih gambar lembar jawab",
            type=["jpg", "jpeg", "png", "bmp"],
            help="Ambil foto lembar jawab dengan pencahayaan cukup"
        )
        
        if uploaded_file:
            # Save temporary file
            temp_path = f"uploads/temp_{datetime.now().timestamp()}.jpg"
            os.makedirs("uploads", exist_ok=True)
            
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Display image
            image = Image.open(uploaded_file)
            st.image(image, caption="Gambar Lembar Jawab", use_column_width=True)
            
            # Show image info
            img_array = cv2.imread(temp_path)
            if img_array is not None:
                height, width = img_array.shape[:2]
                st.info(f"📐 Ukuran Gambar: {width}x{height} pixels")
    
    with col2:
        st.subheader("2. Pilih Kunci Jawaban")
        
        # Get all answer keys from database
        answer_keys = st.session_state.database.get_all_answer_keys()
        
        if answer_keys:
            key_names = [f"{k['name']} ({k['subject']})" if k['subject'] else k['name'] 
                        for k in answer_keys]
            selected_key_idx = st.selectbox(
                "Pilih Kunci Jawaban:",
                range(len(answer_keys)),
                format_func=lambda i: key_names[i]
            )
            selected_key = answer_keys[selected_key_idx]
            st.success(f"✅ Kunci: {selected_key['answer_key']}")
        else:
            st.warning("⚠️ Belum ada kunci jawaban. Buat di menu 'Manajemen Kunci Jawaban'")
            selected_key = None
    
    st.divider()
    
    if uploaded_file and selected_key:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            student_name = st.text_input(
                "Nama Siswa (opsional):",
                help="Opsional - untuk laporan"
            )
        
        with col2:
            student_class = st.text_input(
                "Kelas (opsional):",
                help="Contoh: VI A"
            )
        
        with col3:
            student_no = st.text_input(
                "No. Induk (opsional):",
                help="Nomor absen atau NIS"
            )
        
        st.divider()
        
        if st.button("🔄 Mulai Koreksi", key="start_correction", use_container_width=True):
            with st.spinner("🔄 Memproses lembar jawab..."):
                # Process image
                processor = st.session_state.processor
                result = processor.process_full(temp_path, selected_key['answer_key'])
                
                # Display results
                if result['success']:
                    st.session_state.current_result = result
                    
                    st.markdown("<div class='success-box'><strong>✅ Koreksi Berhasil!</strong></div>", 
                               unsafe_allow_html=True)
                    
                    # Display scores
                    grading = result['grading']
                    
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Skor", f"{grading['score']}/{grading['total']}")
                    with col2:
                        st.metric("Persentase", f"{grading['percentage']:.1f}%")
                    with col3:
                        st.metric("Grade", grading['grade'])
                    with col4:
                        st.metric("Status", "✅ Selesai")
                    
                    st.divider()
                    
                    # Detailed answers
                    st.subheader("📝 Detail Jawaban")
                    
                    # Create table for display
                    details = grading['details']
                    
                    # Display in columns
                    cols = st.columns(4)
                    for i, detail in enumerate(details):
                        col_idx = i % 4
                        with cols[col_idx]:
                            if detail['is_correct']:
                                st.write(f"✅ No. {detail['question']}: {detail['student_answer']}")
                            else:
                                st.write(
                                    f"❌ No. {detail['question']}: "
                                    f"{detail['student_answer']} (Seharusnya: {detail['correct_answer']})"
                                )
                    
                    st.divider()
                    
                    # Save to database
                    if st.button("💾 Simpan Hasil", key="save_result", use_container_width=True):
                        # Add student if provided
                        student_id = None
                        if student_name:
                            success, student_id, msg = st.session_state.database.add_student(
                                student_name, student_class, student_no
                            )
                        
                        # Save result
                        success, result_id, msg = st.session_state.database.save_correction_result(
                            student_id=student_id,
                            key_id=selected_key['key_id'],
                            student_answers=result['answers'],
                            score=grading['score'],
                            percentage=grading['percentage'],
                            grade=grading['grade'],
                            image_file=uploaded_file.name,
                            details=grading['details']
                        )
                        
                        if success:
                            st.success(f"✅ Hasil disimpan! (ID: {result_id})")
                        else:
                            st.error(f"❌ Error: {msg}")
                
                else:
                    st.error(f"❌ Koreksi Gagal: {result['message']}")
                    
                    # Display debug info
                    with st.expander("🔧 Debug Info"):
                        st.write("Steps:")
                        for step, info in result['steps'].items():
                            st.write(f"  - {step}: {info['message']}")

# ===== HALAMAN: MANAJEMEN SISWA =====
elif menu == "👥 Manajemen Siswa":
    st.header("👥 Manajemen Data Siswa")
    
    tab1, tab2 = st.tabs(["Daftar Siswa", "Tambah Siswa"])
    
    with tab1:
        st.subheader("📋 Daftar Siswa")
        
        students = st.session_state.database.get_all_students()
        
        if students:
            # Create dataframe for display
            import pandas as pd
            df = pd.DataFrame(students)
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            st.info(f"Total Siswa: {len(students)}")
        else:
            st.info("📭 Belum ada data siswa")
    
    with tab2:
        st.subheader("➕ Tambah Siswa Baru")
        
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Nama Siswa *")
        
        with col2:
            class_name = st.text_input("Kelas (Contoh: VI A)")
        
        col1, col2 = st.columns(2)
        
        with col1:
            no_nis = st.text_input("No. Induk / NIS")
        
        with col2:
            st.write("")  # Placeholder
        
        if st.button("➕ Tambah Siswa", use_container_width=True):
            if name:
                success, student_id, msg = st.session_state.database.add_student(
                    name, class_name, no_nis
                )
                
                if success:
                    st.success(f"✅ {msg} (ID: {student_id})")
                else:
                    st.error(f"❌ {msg}")
            else:
                st.error("❌ Nama siswa harus diisi!")

# ===== HALAMAN: MANAJEMEN KUNCI JAWABAN =====
elif menu == "🔑 Manajemen Kunci Jawaban":
    st.header("🔑 Manajemen Kunci Jawaban")
    
    tab1, tab2 = st.tabs(["Daftar Kunci", "Tambah Kunci"])
    
    with tab1:
        st.subheader("📋 Daftar Kunci Jawaban")
        
        keys = st.session_state.database.get_all_answer_keys()
        
        if keys:
            import pandas as pd
            
            # Format for display
            display_data = []
            for k in keys:
                display_data.append({
                    'ID': k['key_id'],
                    'Nama': k['name'],
                    'Mata Pelajaran': k['subject'] or '-',
                    'Kunci Jawaban': k['answer_key'],
                    'Total Soal': k['total_questions'],
                    'Tanggal': k['created_at']
                })
            
            df = pd.DataFrame(display_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("📭 Belum ada kunci jawaban")
    
    with tab2:
        st.subheader("➕ Tambah Kunci Jawaban Baru")
        
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Nama Kunci *", placeholder="Contoh: Soal Ujian Tengah Semester")
        
        with col2:
            subject = st.text_input("Mata Pelajaran (opsional)", placeholder="Contoh: Bahasa Indonesia")
        
        st.subheader("Input Kunci Jawaban")
        st.info(f"Masukkan {config.TOTAL_QUESTIONS} karakter (A/B/C/D)")
        
        answer_key = st.text_input(
            "Kunci Jawaban *",
            placeholder="Contoh: ABCDABCDABCDABCDABCDABCDABCDABCDABCDABCD",
            help=f"Masukkan {config.TOTAL_QUESTIONS} karakter untuk 40 soal"
        )
        
        if answer_key:
            # Validate and show preview
            valid, msg = utils.validate_answer_key(answer_key)
            
            if valid:
                st.success("✅ Kunci valid!")
                
                # Show preview
                with st.expander("👁️ Pratinjau Kunci"):
                    # Display in rows
                    preview_text = ""
                    for i in range(0, len(msg), 10):
                        preview_text += f"Soal {i+1:2d}-{min(i+10, len(msg)):2d}: {msg[i:i+10]}\n"
                    st.code(preview_text)
            else:
                st.error(f"❌ {msg}")
        
        if st.button("➕ Simpan Kunci Jawaban", use_container_width=True):
            if name and answer_key:
                valid, validated_key = utils.validate_answer_key(answer_key)
                
                if valid:
                    success, key_id, msg = st.session_state.database.add_answer_key(
                        name, validated_key, subject, config.TOTAL_QUESTIONS
                    )
                    
                    if success:
                        st.success(f"✅ {msg} (ID: {key_id})")
                    else:
                        st.error(f"❌ {msg}")
                else:
                    st.error(f"❌ {validated_key}")
            else:
                st.error("❌ Nama dan kunci jawaban harus diisi!")

# ===== HALAMAN: LAPORAN & STATISTIK =====
elif menu == "📊 Laporan & Statistik":
    st.header("📊 Laporan & Statistik")
    
    tab1, tab2, tab3 = st.tabs(["Ringkasan", "Per Kelas", "Detail"])
    
    with tab1:
        st.subheader("📈 Ringkasan Statistik")
        
        stats = st.session_state.database.get_statistics_summary()
        
        if stats and stats['total_corrections']:
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                st.metric("Total Siswa", stats['total_students'] or 0)
            with col2:
                st.metric("Total Koreksi", stats['total_corrections'] or 0)
            with col3:
                avg_pct = stats['avg_percentage'] or 0
                st.metric("Rata-rata", f"{avg_pct:.1f}%")
            with col4:
                max_pct = stats['max_percentage'] or 0
                st.metric("Tertinggi", f"{max_pct:.1f}%")
            with col5:
                min_pct = stats['min_percentage'] or 0
                st.metric("Terendah", f"{min_pct:.1f}%")
        else:
            st.info("📭 Belum ada data koreksi")
    
    with tab2:
        st.subheader("📊 Statistik Per Kelas")
        
        students = st.session_state.database.get_all_students()
        classes = list(set([s['class'] for s in students if s['class']]))
        
        if classes:
            selected_class = st.selectbox("Pilih Kelas:", classes)
            
            class_stats = st.session_state.database.get_class_statistics(selected_class)
            
            if class_stats and class_stats['total_tests']:
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Total Ujian", class_stats['total_tests'] or 0)
                with col2:
                    avg = class_stats['avg_percentage'] or 0
                    st.metric("Rata-rata", f"{avg:.1f}%")
                with col3:
                    max_p = class_stats['max_percentage'] or 0
                    st.metric("Tertinggi", f"{max_p:.1f}%")
                with col4:
                    min_p = class_stats['min_percentage'] or 0
                    st.metric("Terendah", f"{min_p:.1f}%")
            else:
                st.info("📭 Belum ada data untuk kelas ini")
        else:
            st.info("📭 Belum ada data siswa dengan kelas")
    
    with tab3:
        st.subheader("📋 Detail Hasil Koreksi")
        
        results = st.session_state.database.get_all_results(limit=100)
        
        if results:
            import pandas as pd
            
            display_data = []
            for r in results:
                display_data.append({
                    'ID': r['result_id'],
                    'Tanggal': r['correction_date'],
                    'Skor': f"{r['score']}/{r['total_questions']}",
                    'Persentase': f"{r['percentage']:.1f}%",
                    'Grade': r['grade']
                })
            
            df = pd.DataFrame(display_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("📭 Belum ada hasil koreksi")

# ===== HALAMAN: BANTUAN =====
elif menu == "ℹ️ Bantuan":
    st.header("ℹ️ Bantuan & Panduan")
    
    with st.expander("❓ Pertanyaan Umum", expanded=True):
        st.markdown("""
        **Q: Bagaimana cara menggunakan sistem ini?**
        
        A: Ikuti langkah berikut:
        1. Buka menu "Koreksi Lembar Jawab"
        2. Upload gambar lembar jawab siswa
        3. Pilih kunci jawaban yang sesuai
        4. Klik "Mulai Koreksi"
        5. Sistem akan otomatis mendeteksi dan mengoreksi
        6. Simpan hasil jika diperlukan
        
        ---
        
        **Q: Gambar seperti apa yang ideal?**
        
        A: Gambar harus:
        - Jelas dan tidak blur
        - Pencahayaan cukup (tidak terlalu gelap/terang)
        - Lembar tidak miring/terpotong
        - Resolusi minimum 800x600
        
        ---
        
        **Q: Bagaimana jika hasil koreksi salah?**
        
        A: Kemungkinan penyebab:
        - Lembar kurang jelas saat difoto
        - Siswa mengisi tidak rapi/penuh
        - Tinta/pensil terlalu tipis
        
        Solusi:
        - Ambil foto ulang dengan kualitas lebih baik
        - Ajak siswa mengisi dengan lebih rapi
        """)
    
    with st.expander("📸 Tips Pengambilan Foto"):
        st.markdown("""
        **Lighting (Pencahayaan):**
        - Gunakan cahaya alami atau LED yang merata
        - Hindari bayangan di atas lembar
        - Jangan gunakan flash langsung
        
        **Posisi Kamera:**
        - Posisikan kamera tegak lurus dengan lembar
        - Pastikan semua bagian lembar terlihat
        - Hindari sudut yang terlalu miring
        
        **Kualitas Gambar:**
        - Gunakan resolusi tertinggi
        - Fokus pada area jawaban (Section I)
        - Crop jika perlu, tapi jangan terlalu ketat
        """)
    
    with st.expander("⚙️ Troubleshooting"):
        st.markdown("""
        **Masalah: Sistem tidak bisa mendeteksi kotak jawaban**
        
        Solusi:
        - Ambil foto lembar dengan lebih jelas
        - Pastikan pencahayaan merata
        - Gunakan template resmi sekolah
        
        ---
        
        **Masalah: Hasil koreksi tidak akurat**
        
        Solusi:
        - Pastikan kunci jawaban benar
        - Periksa apakah siswa mengisi dengan rapi
        - Ambil foto ulang dengan kualitas lebih baik
        
        ---
        
        **Masalah: Sistem crash/error**
        
        Solusi:
        - Refresh halaman
        - Gunakan file gambar yang lebih kecil
        - Hubungi administrator
        """)
    
    with st.expander("📞 Kontak Support"):
        st.markdown("""
        **SDN 2 Pusporenggo**
        
        Alamat: Ngemplak Rt. 03 Rw. 03 Pusporenggo, Musuk, Boyolali
        
        Untuk bantuan teknis, silakan hubungi administrator sistem.
        
        **Versi Sistem:** 1.0.0
        """)

# ===== FOOTER =====
st.divider()
st.markdown("""
<div style="text-align: center; color: #7f8c8d; font-size: 12px; margin-top: 30px;">
    <p>Sistem Pengkoreksi Lembar Jawab - SDN 2 Pusporenggo</p>
    <p>© 2024 | Versi 1.0.0</p>
</div>
""", unsafe_allow_html=True)
