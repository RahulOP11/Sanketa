import cv2
import numpy as np

# Custom cipher mapping
CIPHER_MAP = {
    '18': 'A', '16': 'B', '17': 'C', '22': 'D', '21': 'E', '23': 'F',
    '24': 'G', '26': 'H', '19': 'I', '20': 'J', '25': 'K', '14': 'L',
    '12': 'M', '09': 'N', '08': 'O', '04': 'P', '03': 'Q', '02': 'R',
    '01': 'S', '05': 'T', '06': 'U', '07': 'V', '10': 'W', '11': 'X',
    '13': 'Y', '15': 'Z'
}

def decode_number_string(number_string):
    """
    Decodes a string of numbers into characters using the CIPHER_MAP.
    Groups the numbers by 2.
    Example: '0821141408' -> '08', '21', '14', '14', '08' -> 'HELLO'
    """
    decoded_text = []
    pairs = [number_string[i:i+2] for i in range(0, len(number_string), 2)]
    
    for pair in pairs:
        if pair in CIPHER_MAP:
            decoded_text.append(CIPHER_MAP[pair])
        else:
            decoded_text.append('?') # Unknown mapping
            
    return " ".join(decoded_text), pairs

def extract_digits_from_image(image_bytes, model, predict_func):
    """
    Preprocesses the image, finds digit contours, extracts each digit,
    and runs it through the model to predict the number.
    Returns the recognized number string and the processed image with bounding boxes.
    """
    # Convert bytes to cv2 image
    np_arr = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    
    if image is None:
        raise ValueError("Could not decode image.")
        
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Blur and threshold
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Use Otsu's thresholding to handle different lighting
    # Ensure digits are white on black background for contour extraction
    _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    # Find contours
    contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Filter contours based on size to remove noise
    digit_contours = []
    for c in contours:
        (x, y, w, h) = cv2.boundingRect(c)
        if w >= 5 and h >= 15: # Minimum size threshold
            digit_contours.append(c)
            
    # Group contours into rows and sort each row left to right
    bounding_boxes = [cv2.boundingRect(c) for c in digit_contours]
    contours_with_boxes = list(zip(digit_contours, bounding_boxes))
    
    # Sort by center y-coordinate first
    contours_with_boxes.sort(key=lambda x: x[1][1] + (x[1][3] / 2.0))
    
    sorted_digits = []
    current_row = []
    
    # Dynamic row tolerance based on average height
    avg_h = sum([b[3] for b in bounding_boxes]) / len(bounding_boxes) if bounding_boxes else 15
    row_tolerance = max(avg_h * 0.75, 20)
    
    for cb in contours_with_boxes:
        if not current_row:
            current_row.append(cb)
        else:
            cy = cb[1][1] + (cb[1][3] / 2.0)
            avg_cy = sum([item[1][1] + (item[1][3] / 2.0) for item in current_row]) / len(current_row)
            if abs(cy - avg_cy) < row_tolerance:
                current_row.append(cb)
            else:
                current_row.sort(key=lambda x: x[1][0])
                sorted_digits.extend([item[0] for item in current_row])
                current_row = [cb]
    
    if current_row:
        current_row.sort(key=lambda x: x[1][0])
        sorted_digits.extend([item[0] for item in current_row])
        
    digit_contours = sorted_digits
    
    recognized_digits = []
    output_image = image.copy()
    
    for c in digit_contours:
        (x, y, w, h) = cv2.boundingRect(c)
        
        # Draw bounding box for visualization
        cv2.rectangle(output_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        # Extract the region of interest (ROI)
        roi = thresh[y:y + h, x:x + w]
        
        # Pad the ROI to make it square, preserving aspect ratio
        size = max(w, h)
        padded_roi = np.zeros((size + 10, size + 10), dtype=np.uint8)
        
        # Calculate offsets to center the ROI
        y_offset = (size + 10 - h) // 2
        x_offset = (size + 10 - w) // 2
        padded_roi[y_offset:y_offset + h, x_offset:x_offset + w] = roi
        
        # Resize to 28x28 (MNIST format)
        resized_roi = cv2.resize(padded_roi, (28, 28), interpolation=cv2.INTER_AREA)
        
        # Predict the digit
        digit = predict_func(model, resized_roi)
        recognized_digits.append(str(digit))
        
        # Put predicted text on the output image
        cv2.putText(output_image, str(digit), (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        
    number_string = "".join(recognized_digits)
    return number_string, output_image
