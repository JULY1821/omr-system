"""
Modul pemrosesan gambar OMR (Optical Mark Recognition)
Mendeteksi dan mengekstraksi jawaban dari lembar jawab siswa
"""

import cv2
import numpy as np
import imutils
from imutils import contours as imutils_contours
import config
from src import utils

class OMRProcessor:
    """Class untuk memproses lembar jawab siswa"""
    
    def __init__(self):
        self.original_image = None
        self.processed_image = None
        self.gray_image = None
        self.thresh_image = None
        self.detected_boxes = []
        self.debug_info = {}
        
    def load_image(self, image_path):
        """
        Load gambar dari file
        Args:
            image_path: Path ke file gambar
        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            self.original_image = cv2.imread(image_path)
            
            if self.original_image is None:
                return False, "Gagal membaca file gambar"
            
            # Validasi ukuran gambar
            height, width = self.original_image.shape[:2]
            if width < config.MIN_IMAGE_WIDTH or height < config.MIN_IMAGE_HEIGHT:
                return False, f"Gambar terlalu kecil. Minimum: {config.MIN_IMAGE_WIDTH}x{config.MIN_IMAGE_HEIGHT}"
            
            if width > config.MAX_IMAGE_WIDTH or height > config.MAX_IMAGE_HEIGHT:
                return False, f"Gambar terlalu besar. Maksimum: {config.MAX_IMAGE_WIDTH}x{config.MAX_IMAGE_HEIGHT}"
            
            utils.log_info(f"Gambar berhasil dimuat: {width}x{height}")
            self.debug_info['original_size'] = (width, height)
            return True, "Gambar berhasil dimuat"
            
        except Exception as e:
            utils.log_error(f"Error loading image: {str(e)}")
            return False, f"Error: {str(e)}"
    
    def preprocess_image(self):
        """
        Persiapan gambar untuk deteksi
        - Konversi ke grayscale
        - Apply blur untuk mengurangi noise
        - Apply threshold adaptif
        """
        try:
            if self.original_image is None:
                return False, "Gambar belum dimuat"
            
            # 1. Konversi ke grayscale
            self.gray_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
            
            # 2. Apply Gaussian Blur
            blurred = cv2.GaussianBlur(self.gray_image, config.BLUR_KERNEL, 0)
            
            # 3. Apply Adaptive Threshold
            self.thresh_image = cv2.adaptiveThreshold(
                blurred,
                255,
                cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY,
                config.ADAPTIVE_THRESH_BLOCK_SIZE,
                config.ADAPTIVE_THRESH_CONSTANT
            )
            
            self.processed_image = self.thresh_image.copy()
            utils.log_info("Preprocessing gambar selesai")
            return True, "Preprocessing berhasil"
            
        except Exception as e:
            utils.log_error(f"Error preprocessing: {str(e)}")
            return False, f"Error: {str(e)}"
    
    def detect_answer_boxes(self):
        """
        Deteksi kotak-kotak jawaban dari gambar
        Menggunakan contour detection
        """
        try:
            if self.thresh_image is None:
                return False, "Gambar belum diproses"
            
            # Invert image (kotak hitam menjadi putih)
            inverted = cv2.bitwise_not(self.thresh_image)
            
            # Deteksi kontur
            contours = cv2.findContours(
                inverted.copy(),
                cv2.RETR_TREE,
                cv2.CHAIN_APPROX_SIMPLE
            )
            contours = imutils.grab_contours(contours)
            
            utils.log_info(f"Ditemukan {len(contours)} kontur")
            
            # Filter kontur berdasarkan area
            boxes = []
            for contour in contours:
                area = cv2.contourArea(contour)
                if config.MIN_CONTOUR_AREA < area < config.MAX_CONTOUR_AREA:
                    # Dapatkan bounding box
                    x, y, w, h = cv2.boundingRect(contour)
                    
                    # Hanya ambil kotak yang ukurannya masuk akal
                    if 10 < w < 50 and 10 < h < 50:
                        boxes.append({'x': x, 'y': y, 'w': w, 'h': h, 'area': area})
            
            # Sort boxes berdasarkan posisi (atas ke bawah, kiri ke kanan)
            boxes = sorted(boxes, key=lambda b: (b['y'], b['x']))
            
            self.detected_boxes = boxes
            self.debug_info['detected_boxes'] = len(boxes)
            
            utils.log_info(f"Terdeteksi {len(boxes)} kotak jawaban")
            return True, f"Terdeteksi {len(boxes)} kotak"
            
        except Exception as e:
            utils.log_error(f"Error detecting boxes: {str(e)}")
            return False, f"Error: {str(e)}"
    
    def extract_answers(self):
        """
        Ekstraksi jawaban dari kotak yang terdeteksi
        Menganalisis tingkat kegelapan setiap kotak
        
        Returns:
            tuple: (success: bool, answers: list[int], message: str)
            answers: list of indices (0=A, 1=B, 2=C, 3=D, -1=tidak ada)
        """
        try:
            if not self.detected_boxes or self.thresh_image is None:
                return False, [], "Kotak jawaban belum terdeteksi"
            
            answers = []
            
            # Kelompokkan kotak per soal
            # Lembar punya format khusus dengan 2 kolom dan multiple rows
            
            # Analisis setiap soal
            # Total 40 soal, tapi kotak terdeteksi harus 160 (40 x 4)
            
            if len(self.detected_boxes) < 160:
                utils.log_warning(f"Kotak terdeteksi kurang: {len(self.detected_boxes)} dari 160 diharapkan")
            
            # Group boxes per soal (tiap soal punya 4 kotak untuk pilihan a,b,c,d)
            sorted_boxes = sorted(self.detected_boxes, key=lambda b: (b['y'] // 30, b['x']))
            
            for i in range(0, len(sorted_boxes), 4):
                if i + 3 < len(sorted_boxes):
                    # Ambil 4 kotak untuk 1 soal
                    question_boxes = sorted_boxes[i:i+4]
                    
                    # Analisis tingkat kegelapan masing-masing pilihan
                    darkness_scores = []
                    for box in question_boxes:
                        darkness = self._calculate_darkness(box)
                        darkness_scores.append(darkness)
                    
                    # Tentukan pilihan yang dipilih (tertinggi kegelapannya)
                    max_darkness_idx = np.argmax(darkness_scores)
                    max_darkness = darkness_scores[max_darkness_idx]
                    
                    # Jika kegelapan > threshold, dianggap diisi
                    if max_darkness > config.FILL_THRESHOLD:
                        answers.append(max_darkness_idx)
                    else:
                        answers.append(-1)  # Tidak ada pilihan yang jelas
            
            self.debug_info['extracted_answers'] = len(answers)
            utils.log_info(f"Ekstraksi {len(answers)} jawaban berhasil")
            return True, answers, f"Ekstraksi {len(answers)} jawaban berhasil"
            
        except Exception as e:
            utils.log_error(f"Error extracting answers: {str(e)}")
            return False, [], f"Error: {str(e)}"
    
    def _calculate_darkness(self, box):
        """
        Hitung tingkat kegelapan area kotak
        Returns: float (0.0 - 1.0, semakin tinggi = semakin gelap)
        """
        x, y, w, h = box['x'], box['y'], box['w'], box['h']
        
        # Ambil region dalam threshold image
        roi = self.thresh_image[y:y+h, x:x+w]
        
        if roi.size == 0:
            return 0.0
        
        # Hitung rasio pixel hitam (0 value dalam threshold)
        # Di threshold image, object adalah 255 dan background adalah 0
        black_pixels = cv2.countNonZero(cv2.bitwise_not(roi))
        total_pixels = roi.size
        
        darkness = black_pixels / total_pixels
        return darkness
    
    def grade_answers(self, student_answers, answer_key):
        """
        Bandingkan jawaban siswa dengan kunci jawaban
        
        Args:
            student_answers: list of answer indices
            answer_key: string 'ABCD...' atau list of indices
        
        Returns:
            dict: hasil grading dengan detail
        """
        try:
            # Konversi answer key ke indices jika perlu
            if isinstance(answer_key, str):
                key_indices = [ord(c) - ord('A') for c in answer_key.upper() if c in 'ABCD']
            else:
                key_indices = answer_key
            
            # Pastikan panjang sama
            if len(student_answers) != len(key_indices):
                return {
                    'success': False,
                    'score': 0,
                    'total': 0,
                    'percentage': 0,
                    'message': f"Panjang jawaban tidak sesuai: {len(student_answers)} vs {len(key_indices)}"
                }
            
            # Hitung skor
            correct = 0
            details = []
            
            for i, (student, key) in enumerate(zip(student_answers, key_indices)):
                is_correct = student == key
                if is_correct:
                    correct += 1
                
                details.append({
                    'question': i + 1,
                    'student_answer': chr(ord('A') + student) if student >= 0 else '-',
                    'correct_answer': chr(ord('A') + key),
                    'is_correct': is_correct
                })
            
            percentage = (correct / len(key_indices)) * 100
            
            result = {
                'success': True,
                'score': correct,
                'total': len(key_indices),
                'percentage': round(percentage, 2),
                'grade': utils.get_grade(percentage),
                'details': details,
                'message': f"Skor: {correct}/{len(key_indices)} ({percentage:.1f}%)"
            }
            
            utils.log_info(result['message'])
            return result
            
        except Exception as e:
            utils.log_error(f"Error grading: {str(e)}")
            return {
                'success': False,
                'message': f"Error: {str(e)}"
            }
    
    def process_full(self, image_path, answer_key):
        """
        Proses lengkap: load -> preprocess -> deteksi -> ekstraksi -> grade
        
        Args:
            image_path: path ke gambar
            answer_key: kunci jawaban
        
        Returns:
            dict: hasil proses lengkap
        """
        result = {
            'success': False,
            'steps': {},
            'answers': [],
            'grading': None,
            'message': ''
        }
        
        try:
            # Step 1: Load image
            success, msg = self.load_image(image_path)
            result['steps']['load'] = {'success': success, 'message': msg}
            if not success:
                result['message'] = msg
                return result
            
            # Step 2: Preprocess
            success, msg = self.preprocess_image()
            result['steps']['preprocess'] = {'success': success, 'message': msg}
            if not success:
                result['message'] = msg
                return result
            
            # Step 3: Detect boxes
            success, msg = self.detect_answer_boxes()
            result['steps']['detect'] = {'success': success, 'message': msg}
            if not success:
                result['message'] = msg
                return result
            
            # Step 4: Extract answers
            success, answers, msg = self.extract_answers()
            result['steps']['extract'] = {'success': success, 'message': msg}
            result['answers'] = answers
            if not success:
                result['message'] = msg
                return result
            
            # Step 5: Grade
            grading = self.grade_answers(answers, answer_key)
            result['grading'] = grading
            
            if grading['success']:
                result['success'] = True
                result['message'] = grading['message']
            else:
                result['message'] = grading['message']
            
            return result
            
        except Exception as e:
            utils.log_error(f"Error in full processing: {str(e)}")
            result['message'] = f"Error: {str(e)}"
            return result
    
    def get_debug_visualization(self):
        """
        Buat visualisasi untuk debugging
        Menampilkan kotak yang terdeteksi di gambar
        """
        if self.original_image is None:
            return None
        
        # Copy image original untuk visualisasi
        vis = self.original_image.copy()
        
        # Draw detected boxes
        for i, box in enumerate(self.detected_boxes):
            x, y, w, h = box['x'], box['y'], box['w'], box['h']
            cv2.rectangle(vis, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(vis, str(i), (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 0), 1)
        
        return vis
