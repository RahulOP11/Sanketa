# SANKETA // VISION_V1.0 👁️‍🗨️

> `[SYSTEM_INIT]: AI-BASED DECODER ACTIVE`

Sanketa Vision is a Cyberpunk-styled Streamlit application designed for recovering data from visual anomalies. It features dual processing modes to decrypt handwritten numeric ciphers using Neural Networks and reconstruct laterally distorted (mirrored) physical text streams.

![Cyber Vision Interface](assets/banner.png) <!-- Replace this with an actual screenshot path when you upload images! -->

## ⚡ Features

### `[PROTOCOL 1: CIPHER DECODER]`
Translates numeric anomalies utilizing an integrated MNIST Multi-Layer Perceptron. Upload an image containing a handwritten numeric sequence (A=18, B=16...), and the system will attempt to:
* Detect and isolate handwritten characters using OpenCV bounding box extraction
* Evaluate vectors utilizing a trained neural model
* Decode numerical values into plaintext string formats
* Generate a full `[DATALINK_REPORT.pdf]` of the translated arrays and plaintext

### `[PROTOCOL 2: MIRROR RECOGNITION]`
Reverses horizontal spatial distortion on input imagery and applies OCR payload extraction.
* Uses image inversion protocols (horizontal flip)
* Connects through the Tesseract OCR engine dynamically
* Recovers text corrupted by physical mirror distortion

## 🛠️ Installation & Execution

1. **Clone the repository (or download the files):**
   ```bash
   git clone https://github.com/RahulOP11/Sanketa.git
   cd Sanketa/SanketaVision
   ```

2. **Install all required dependencies:**
   It is recommended to run this within a Virtual Environment (`venv`):
   ```bash
   pip install -r requirements.txt
   ```

3. **Requirements specific to OCR:**
   - **Tesseract OCR** must be installed on your system. 
   - Windows installation defaults to `C:\Program Files\Tesseract-OCR\tesseract.exe`. Ensure it is installed there, or point to it in the **Advanced OCR Engine Configuration** within the UI.

4. **Initialize the Server Matrix:**
   ```bash
   streamlit run app.py
   ```

## 📸 Screenshots

*Create an `assets/` folder in this repository, place your screenshot pictures there, and update the links below!*

### The Main Interface
![Main Interface](assets/main_ui.png)

### Cipher Extraction Active
![Cipher Decoding](assets/cipher_decode.png)

### Mirror Protocol Active
![Mirror Recognition](assets/mirror_protocol.png)

---
<p align="center" style="color: #00FF41; font-family: monospace;">[END OF TRANSMISSION] // SANKETA_VISION_V1.0 // CONNECTION_SECURE</p>
