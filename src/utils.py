"""
Fungsi utility untuk sistem OMR
"""

import os
import logging
from datetime import datetime
import config

# Setup logging
def setup_logging():
    """Inisialisasi logging system"""
    os.makedirs('logs', exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(config.LOG_FILE),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

logger = setup_logging()

# ===== VALIDASI INPUT =====

def validate_image_file(file_path):
    """
    Validasi file gambar
    Returns: (valid: bool, message: str)
    """
    if not os.path.exists(file_path):
        return False, "File tidak ditemukan"
    
    # Check extension
    ext = os.path.splitext(file_path)[1].lower()
    if ext not in [f'.{e}' for e in config.ALLOWED_EXTENSIONS]:
        return False, f"Format file tidak didukung. Gunakan: {', '.join(config.ALLOWED_EXTENSIONS)}"
    
    # Check file size
    file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
    if file_size_mb > config.MAX_FILE_SIZE_MB:
        return False, f"Ukuran file terlalu besar (max: {config.MAX_FILE_SIZE_MB}MB)"
    
    return True, "OK"

def validate_answer_key(answer_key):
    """
    Validasi kunci jawaban
    Returns: (valid: bool, message: str)
    """
    if not answer_key:
        return False, "Kunci jawaban tidak boleh kosong"
    
    # Remove spaces and convert to lowercase
    answer_key = answer_key.replace(' ', '').lower()
    
    # Check length
    if len(answer_key) != config.TOTAL_QUESTIONS:
        return False, f"Kunci harus {config.TOTAL_QUESTIONS} karakter, Anda masuk {len(answer_key)}"
    
    # Check characters
    valid_chars = set(config.CHOICES)
    for char in answer_key:
        if char not in valid_chars:
            return False, f"Karakter '{char}' tidak valid. Gunakan: {', '.join(config.CHOICES)}"
    
    return True, answer_key.upper()

def validate_student_name(name):
    """Validasi nama siswa"""
    if not name or len(name.strip()) == 0:
        return False, "Nama siswa tidak boleh kosong"
    
    if len(name) > 100:
        return False, "Nama siswa terlalu panjang (max: 100 karakter)"
    
    return True, name.strip()

# ===== FORMAT DATA =====

def format_answer_list(answers):
    """
    Konversi list jawaban ke string
    Input: [0, 2, 1, 3, ...] (index 0-3 untuk a-d)
    Output: "ACBD..."
    """
    choice_map = {0: 'A', 1: 'B', 2: 'C', 3: 'D', -1: '-'}
    return ''.join([choice_map.get(ans, '-') for ans in answers])

def format_score(score, total):
    """Format skor menjadi persentase dan nilai"""
    percentage = (score / total * 100) if total > 0 else 0
    return {
        'score': score,
        'total': total,
        'percentage': round(percentage, 2),
        'grade': get_grade(percentage)
    }

def get_grade(percentage):
    """
    Konversi persentase ke grade/nilai
    Skala: A (90-100), B (80-89), C (70-79), D (60-69), E (<60)
    """
    if percentage >= 90:
        return 'A'
    elif percentage >= 80:
        return 'B'
    elif percentage >= 70:
        return 'C'
    elif percentage >= 60:
        return 'D'
    else:
        return 'E'

# ===== HELPER FUNCTIONS =====

def create_directories():
    """Buat direktori yang diperlukan"""
    directories = [
        'logs',
        'data',
        'data/results',
        'templates',
        'uploads'
    ]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

def get_timestamp():
    """Dapatkan timestamp saat ini"""
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def compare_answers(student_answers, answer_key):
    """
    Bandingkan jawaban siswa dengan kunci
    Returns: list of (question_num, student_ans, answer_key, is_correct)
    """
    results = []
    for i, (student, key) in enumerate(zip(student_answers, answer_key)):
        is_correct = student == key
        results.append({
            'question': i + 1,
            'student_answer': student,
            'correct_answer': key,
            'is_correct': is_correct
        })
    return results

# ===== LOGGING HELPERS =====

def log_info(message):
    """Log informasi"""
    logger.info(message)

def log_error(message):
    """Log error"""
    logger.error(message)

def log_warning(message):
    """Log warning"""
    logger.warning(message)

def log_debug(message):
    """Log debug info"""
    if config.DEBUG_MODE:
        logger.debug(message)
