import cv2
import pytesseract
import numpy as np

def setup_tesseract_path(path_to_tesseract):
    """
    Sets the tesseract executable path.
    Example: path_to_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    """
    pytesseract.pytesseract.tesseract_cmd = path_to_tesseract

def flip_image_horizontally(image_bytes):
    """
    Takes raw image bytes, converts them to an OpenCV image,
    and flips it horizontally.
    """
    # Convert bytes to numpy array
    np_arr = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    
    if image is None:
        raise ValueError("Could not decode image.")
        
    # Flip the image horizontally (1 = horizontal flip)
    flipped_image = cv2.flip(image, 1)
    return flipped_image

def extract_text_from_image(cv2_image):
    """
    Uses Tesseract OCR to extract text from an OpenCV image.
    """
    # Convert image to RGB (OpenCV uses BGR by default, Tesseract expects RGB)
    rgb_image = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB)
    
    # Optional preprocessing: grayscale, thresholding
    # gray = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2GRAY)
    # _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    
    text = pytesseract.image_to_string(rgb_image)
    return text.strip()

def process_mirror_image(image_bytes):
    """
    Master function to handle the entire mirror handwriting process.
    """
    flipped_cv_img = flip_image_horizontally(image_bytes)
    extracted_text = extract_text_from_image(flipped_cv_img)
    return flipped_cv_img, extracted_text
