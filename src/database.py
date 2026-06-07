"""
Modul database untuk sistem OMR
Mengelola data siswa dan hasil koreksi
"""

import sqlite3
import json
from datetime import datetime
import config
from src import utils

class OMRDatabase:
    """Class untuk manajemen database sistem OMR"""
    
    def __init__(self, db_path=None):
        self.db_path = db_path or config.DATABASE_PATH
        self.init_database()
    
    def init_database(self):
        """Inisialisasi database dengan tabel-tabel yang diperlukan"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Tabel siswa
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS students (
                    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    class TEXT,
                    no_nis TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Tabel kunci jawaban (per mata pelajaran/soal set)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS answer_keys (
                    key_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    subject TEXT,
                    answer_key TEXT NOT NULL,
                    total_questions INTEGER DEFAULT 40,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Tabel hasil koreksi
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS correction_results (
                    result_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id INTEGER,
                    key_id INTEGER,
                    student_answers TEXT NOT NULL,
                    score INTEGER,
                    total_questions INTEGER DEFAULT 40,
                    percentage REAL,
                    grade TEXT,
                    image_file TEXT,
                    correction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    details TEXT,
                    FOREIGN KEY (student_id) REFERENCES students(student_id),
                    FOREIGN KEY (key_id) REFERENCES answer_keys(key_id)
                )
            ''')
            
            # Tabel session/batch koreksi
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS correction_sessions (
                    session_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_name TEXT,
                    subject TEXT,
                    exam_date TEXT,
                    total_students INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    completed_at TIMESTAMP
                )
            ''')
            
            conn.commit()
            conn.close()
            utils.log_info("Database initialized successfully")
            return True
            
        except Exception as e:
            utils.log_error(f"Error initializing database: {str(e)}")
            return False
    
    # ===== SISWA (STUDENTS) =====
    
    def add_student(self, name, class_name='', no_nis=''):
        """
        Tambah data siswa baru
        Returns: (success: bool, student_id: int, message: str)
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO students (name, class, no_nis)
                VALUES (?, ?, ?)
            ''', (name, class_name, no_nis))
            
            conn.commit()
            student_id = cursor.lastrowid
            conn.close()
            
            utils.log_info(f"Student added: {name} (ID: {student_id})")
            return True, student_id, "Siswa berhasil ditambahkan"
            
        except Exception as e:
            utils.log_error(f"Error adding student: {str(e)}")
            return False, None, f"Error: {str(e)}"
    
    def get_student(self, student_id):
        """Ambil data siswa berdasarkan ID"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM students WHERE student_id = ?', (student_id,))
            row = cursor.fetchone()
            conn.close()
            
            return dict(row) if row else None
            
        except Exception as e:
            utils.log_error(f"Error getting student: {str(e)}")
            return None
    
    def get_all_students(self):
        """Ambil semua data siswa"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM students ORDER BY name')
            rows = cursor.fetchall()
            conn.close()
            
            return [dict(row) for row in rows]
            
        except Exception as e:
            utils.log_error(f"Error getting students: {str(e)}")
            return []
    
    # ===== KUNCI JAWABAN (ANSWER KEYS) =====
    
    def add_answer_key(self, name, answer_key, subject='', total_questions=40):
        """
        Tambah kunci jawaban baru
        Returns: (success: bool, key_id: int, message: str)
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO answer_keys (name, subject, answer_key, total_questions)
                VALUES (?, ?, ?, ?)
            ''', (name, subject, answer_key.upper(), total_questions))
            
            conn.commit()
            key_id = cursor.lastrowid
            conn.close()
            
            utils.log_info(f"Answer key added: {name} (ID: {key_id})")
            return True, key_id, "Kunci jawaban berhasil disimpan"
            
        except Exception as e:
            utils.log_error(f"Error adding answer key: {str(e)}")
            return False, None, f"Error: {str(e)}"
    
    def get_answer_key(self, key_id):
        """Ambil kunci jawaban berdasarkan ID"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM answer_keys WHERE key_id = ?', (key_id,))
            row = cursor.fetchone()
            conn.close()
            
            return dict(row) if row else None
            
        except Exception as e:
            utils.log_error(f"Error getting answer key: {str(e)}")
            return None
    
    def get_all_answer_keys(self):
        """Ambil semua kunci jawaban"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM answer_keys ORDER BY created_at DESC')
            rows = cursor.fetchall()
            conn.close()
            
            return [dict(row) for row in rows]
            
        except Exception as e:
            utils.log_error(f"Error getting answer keys: {str(e)}")
            return []
    
    # ===== HASIL KOREKSI (RESULTS) =====
    
    def save_correction_result(self, student_id, key_id, student_answers, 
                              score, percentage, grade, image_file='', details=None):
        """
        Simpan hasil koreksi
        Returns: (success: bool, result_id: int, message: str)
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Convert answers to string if list
            if isinstance(student_answers, list):
                student_answers = ','.join([str(a) for a in student_answers])
            
            # Convert details to JSON if dict
            if isinstance(details, dict):
                details = json.dumps(details)
            
            cursor.execute('''
                INSERT INTO correction_results 
                (student_id, key_id, student_answers, score, percentage, grade, image_file, details)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (student_id, key_id, student_answers, score, percentage, grade, image_file, details or ''))
            
            conn.commit()
            result_id = cursor.lastrowid
            conn.close()
            
            utils.log_info(f"Correction result saved: {result_id}")
            return True, result_id, "Hasil koreksi berhasil disimpan"
            
        except Exception as e:
            utils.log_error(f"Error saving correction result: {str(e)}")
            return False, None, f"Error: {str(e)}"
    
    def get_correction_result(self, result_id):
        """Ambil hasil koreksi berdasarkan ID"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM correction_results WHERE result_id = ?', (result_id,))
            row = cursor.fetchone()
            conn.close()
            
            if row:
                result = dict(row)
                # Parse JSON details
                if result['details']:
                    try:
                        result['details'] = json.loads(result['details'])
                    except:
                        pass
                return result
            return None
            
        except Exception as e:
            utils.log_error(f"Error getting result: {str(e)}")
            return None
    
    def get_student_results(self, student_id):
        """Ambil semua hasil koreksi untuk seorang siswa"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM correction_results 
                WHERE student_id = ? 
                ORDER BY correction_date DESC
            ''', (student_id,))
            
            rows = cursor.fetchall()
            conn.close()
            
            return [dict(row) for row in rows]
            
        except Exception as e:
            utils.log_error(f"Error getting student results: {str(e)}")
            return []
    
    def get_all_results(self, limit=None):
        """Ambil semua hasil koreksi"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            query = 'SELECT * FROM correction_results ORDER BY correction_date DESC'
            if limit:
                query += f' LIMIT {limit}'
            
            cursor.execute(query)
            rows = cursor.fetchall()
            conn.close()
            
            return [dict(row) for row in rows]
            
        except Exception as e:
            utils.log_error(f"Error getting all results: {str(e)}")
            return []
    
    # ===== STATISTIK =====
    
    def get_class_statistics(self, class_name):
        """Ambil statistik hasil untuk satu kelas"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT 
                    COUNT(cr.result_id) as total_tests,
                    AVG(cr.percentage) as avg_percentage,
                    MAX(cr.percentage) as max_percentage,
                    MIN(cr.percentage) as min_percentage,
                    AVG(cr.score) as avg_score
                FROM correction_results cr
                JOIN students s ON cr.student_id = s.student_id
                WHERE s.class = ?
            ''', (class_name,))
            
            row = cursor.fetchone()
            conn.close()
            
            return dict(row) if row else None
            
        except Exception as e:
            utils.log_error(f"Error getting class statistics: {str(e)}")
            return None
    
    def get_statistics_summary(self):
        """Ambil ringkasan statistik keseluruhan"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT 
                    COUNT(DISTINCT student_id) as total_students,
                    COUNT(result_id) as total_corrections,
                    AVG(percentage) as avg_percentage,
                    MAX(percentage) as max_percentage,
                    MIN(percentage) as min_percentage
                FROM correction_results
            ''')
            
            row = cursor.fetchone()
            conn.close()
            
            return dict(row) if row else None
            
        except Exception as e:
            utils.log_error(f"Error getting summary: {str(e)}")
            return None
