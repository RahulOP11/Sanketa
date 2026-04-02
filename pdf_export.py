from fpdf import FPDF
from datetime import datetime

class CyberPDF(FPDF):
    def footer(self):
        self.set_y(-15)
        self.set_font("Courier", size=8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, "[END OF TRANSMISSION]", align="C")

def generate_cipher_report(raw_cypher, grouped_pairs, decoded_text):
    pdf = CyberPDF()
    pdf.add_page()
    
    # Use built-in Courier font
    
    # Header
    pdf.set_font("Courier", style="B", size=16)
    pdf.set_text_color(0, 150, 0)
    pdf.cell(0, 10, "SANKETA // VISION - DECODING REPORT", align="C", ln=True)
    pdf.set_draw_color(0, 150, 0)
    pdf.line(10, 20, 200, 20)
    pdf.ln(10)
    
    # Timestamp
    pdf.set_font("Courier", size=10)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 5, f"TIMESTAMP: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
    pdf.ln(10)
    
    # Content body
    pdf.set_text_color(0, 0, 0)
    
    pdf.set_font("Courier", style="B", size=12)
    pdf.cell(0, 8, ">> RAW CYPHER SEQUENCE:", ln=True)
    pdf.set_font("Courier", size=12)
    pdf.multi_cell(0, 8, str(raw_cypher))
    pdf.ln(5)
    
    pdf.set_font("Courier", style="B", size=12)
    pdf.cell(0, 8, ">> GROUPED DATA ARRAYS:", ln=True)
    pdf.set_font("Courier", size=12)
    grouped_str = " | ".join(grouped_pairs)
    pdf.multi_cell(0, 8, grouped_str)
    pdf.ln(5)
    
    pdf.set_font("Courier", style="B", size=14)
    pdf.set_text_color(0, 120, 0)
    pdf.cell(0, 8, ">> TRANSLATED PLAINTEXT (FINAL):", ln=True)
    pdf.set_font("Courier", style="B", size=16)
    pdf.set_text_color(0, 0, 0)
    
    # Clean up any newlines for the standard fpdf multi_cell
    clean_text = str(decoded_text).replace("\n", " ").strip()
    pdf.multi_cell(0, 10, clean_text)
    
    # Generate bytes
    pdf_bytes = pdf.output()
    return bytes(pdf_bytes)
