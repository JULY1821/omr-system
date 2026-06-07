# Konfigurasi Sistem OMR untuk SDN 2 Pusporenggo

# ===== KONFIGURASI LEMBAR JAWAB =====
TOTAL_QUESTIONS = 40
QUESTIONS_PER_ROW = 20
CHOICES = ['a', 'b', 'c', 'd']
NUM_CHOICES = 4

# ===== LAYOUT KOTAK JAWABAN =====
# Deteksi posisi kotak berdasarkan struktur lembar
ROWS_LEFT_COLUMN = 20  # Soal 1-20
ROWS_RIGHT_COLUMN = 20  # Soal 21-40

# ===== THRESHOLD DETEKSI =====
# Untuk menentukan apakah kotak diisi atau tidak
FILL_THRESHOLD = 0.30  # 30% pixel gelap = dianggap diisi
MIN_FILL_PIXELS = 100  # Minimum pixel yang harus gelap

# ===== PENGOLAHAN GAMBAR =====
BLUR_KERNEL = (5, 5)
ADAPTIVE_THRESH_BLOCK_SIZE = 11
ADAPTIVE_THRESH_CONSTANT = 2
CANNY_THRESHOLD1 = 100
CANNY_THRESHOLD2 = 200

# ===== DETEKSI KONTUR =====
MIN_CONTOUR_AREA = 50
MAX_CONTOUR_AREA = 5000
CONTOUR_APPROXIMATION = 0.02

# ===== KUALITAS GAMBAR =====
MIN_IMAGE_WIDTH = 800
MIN_IMAGE_HEIGHT = 600
MAX_IMAGE_WIDTH = 4000
MAX_IMAGE_HEIGHT = 4000

# ===== DATABASE =====
DATABASE_PATH = 'data/students.db'
RESULTS_EXPORT_PATH = 'data/results/'

# ===== FILE UPLOAD =====
ALLOWED_EXTENSIONS = ['jpg', 'jpeg', 'png', 'bmp']
MAX_FILE_SIZE_MB = 10  # 10 MB

# ===== LOGGING =====
LOG_FILE = 'logs/omr_system.log'
DEBUG_MODE = False

# ===== SEKOLAH INFO =====
SCHOOL_NAME = "SEKOLAH DASAR NEGERI 2 PUSPORENGGO"
SCHOOL_ADDRESS = "Ngemplak Rt. 03 Rw. 03 Pusporenggo, Musuk, Boyolali"
COORDINATOR = "KOORDINATOR PAUD DIKDAS DAN LS KECAMATAN MUSUK"
