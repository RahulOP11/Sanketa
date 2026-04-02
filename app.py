import streamlit as st
import io
import tensorflow as tf
from mirror_decoder import process_mirror_image, setup_tesseract_path
from cipher_decoder import extract_digits_from_image, decode_number_string
from model_utils import get_mnist_model, predict_digit
from pdf_export import generate_cipher_report
from PIL import Image

def initialize_ui():
    st.set_page_config(
        page_title="SANKETA // VISION",
        page_icon="👁️‍🗨️",
        layout="centered",
        initial_sidebar_state="expanded"
    )

    # Injecting Custom CSS for "Cyber Vibes"
    cyber_css = """
    <style>
    /* Neon glow for headers */
    h1, h2, h3 {
        color: #00FF41 !important;
        text-shadow: 0px 0px 8px rgba(0, 255, 65, 0.6);
        font-family: 'Courier New', Courier, monospace;
        animation: glitch 2s linear infinite;
    }
    
    @keyframes glitch{
      2%,64%{ transform: translate(2px,0) skew(0deg); }
      4%,60%{ transform: translate(-2px,0) skew(0deg); }
      62%{ transform: translate(0,0) skew(5deg); }
    }

    /* Cyber buttons */
    .stButton>button {
        border: 1px solid #00FF41 !important;
        color: #00FF41 !important;
        background-color: transparent !important;
        box-shadow: inset 0 0 5px rgba(0,255,65,0.2), 0 0 8px rgba(0,255,65,0.4);
        transition: all 0.3s ease-in-out;
        font-weight: bold;
        position: relative;
        overflow: hidden;
    }
    
    .stButton>button::after {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: rgba(0, 255, 65, 0.1);
        transform: rotate(45deg);
        animation: pulse 3s infinite;
    }

    @keyframes pulse {
        0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(0, 255, 65, 0.7); }
        70% { transform: scale(1); box-shadow: 0 0 0 10px rgba(0, 255, 65, 0); }
        100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(0, 255, 65, 0); }
    }

    .stButton>button:hover {
        background-color: #00FF41 !important;
        color: #0D0D0D !important;
        box-shadow: 0 0 15px rgba(0, 255, 65, 0.8);
    }
    
    /* Global Scanline Overlay */
    body::after {
        content: " ";
        display: block;
        position: fixed;
        top: 0;
        left: 0;
        bottom: 0;
        right: 0;
        background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%), linear-gradient(90deg, rgba(255, 0, 0, 0.06), rgba(0, 255, 0, 0.02), rgba(0, 0, 255, 0.06));
        z-index: 9999;
        background-size: 100% 2px, 3px 100%;
        pointer-events: none;
    }
    
    /* File uploader hover borders and text input */
    section[data-testid="stFileUploadDropzone"] {
        border: 1px dashed #00FF41 !important;
        background-color: #111111 !important;
    }
    
    /* Custom Info text boxes */
    div[data-testid="stAlert"] {
        background-color: #0a2612 !important;
        border-left: 5px solid #00FF41 !important;
        color: #e0e0e0 !important;
    }

    /* Emphasized Text */
    strong {
        color: #00FF41;
    }
    </style>
    """
    st.markdown(cyber_css, unsafe_allow_html=True)
    
    try:
        banner = Image.open(r"C:\Users\Rahul_OP\.gemini\antigravity\brain\9c4c3037-8ef5-4ad4-8ae7-9abc4c5a1d43\cyber_vision_banner_1773068666168.png")
        st.image(banner, use_container_width=True)
    except Exception:
        pass

    st.title("> SANKETA // VISION_V1.0")
    st.markdown("### `[SYSTEM_INIT]: AI-BASED DECODER ACTIVE`")
    st.markdown("---")

    # Mode selection
    mode = st.sidebar.radio(
        "> SELECT_OPERATION_MODE",
        ("[MODE: CIPHER_DECODER]", "[MODE: MIRROR_RECOGNITION]")
    )

    st.sidebar.markdown("---")
    st.sidebar.info(
        "**[PROTOCOL 1: CIPHER]**\nTranslates numeric anomalies (A=18, B=16...) via Neural Network.\n\n"
        "**[PROTOCOL 2: MIRROR]**\nReverses horizontal distortion & applies OCR extraction."
    )

    st.sidebar.markdown("---")
    st.sidebar.markdown("### `>> SYSTEM_STATUS`")
    m_col1, m_col2 = st.sidebar.columns(2)
    m_col1.metric(label="NET_LINK", value="ONLINE", delta="12ms", delta_color="off")
    m_col2.metric(label="ENCRYPT", value="AES-256", delta="SECURE", delta_color="off")
    st.sidebar.metric(label="NEURAL_LOAD", value="42.7%", delta="-2.1%", delta_color="inverse")

    return mode

def render_cipher_mode():
    st.header(">_ CIPHER DECODER MODULE")
    st.write("Upload cipher sequence image for neural processing.")
    
    with st.container():
        uploaded_file = st.file_uploader("[INPUT DATA_STREAM...]", type=["jpg", "jpeg", "png"], key="cipher_uploader")
    
    if uploaded_file is not None:
        st.markdown("---")
        col_img, col_act = st.columns([1, 1])
        with col_img:
            st.image(uploaded_file, caption="[UPLOADED_DATA_FRAGMENTS]", use_container_width=True)
        with col_act:
            st.markdown("### `>> READY FOR EXTRACTION`")
            st.write("Image data loaded into buffer. Awaiting execute command.")
            execute_btn = st.button("INITIATE DECODE SEQUENCE", type="primary", use_container_width=True)
        
        if execute_btn:
            st.markdown("---")
            with st.spinner(">> LOADING NEURAL MATRIX & EXTRACTING..."):
                try:
                    # Load model
                    model = get_mnist_model()
                    
                    # Read image
                    image_bytes = uploaded_file.read()
                    
                    # Process image
                    st.info(">> LOCATING HANDWRITTEN VECTORS...")
                    number_string, processed_img = extract_digits_from_image(image_bytes, model, predict_digit)
                    
                    # Decode
                    decoded_text, pairs = decode_number_string(number_string)
                    
                    st.success("[DECODE_COMPLETE] SEQUENCE BROKEN.")
                    
                    res_col1, res_col2 = st.columns(2)
                    with res_col1:
                        st.subheader(">> TENSOR OUTPUT")
                        st.image(processed_img, channels="BGR", caption="[BOUNDING_BOXES GENERATED]", use_container_width=True)
                    
                    with res_col2:
                        st.subheader(">> DATALINK_RESULTS")
                        st.markdown(f"**RAW CYPHER:** `{number_string}`")
                        st.markdown(f"**GROUPED ARRAYS:** `{' | '.join(pairs)}`")
                        st.info(f"**TRANSLATED PLAINTEXT:** {decoded_text}")
                        
                        st.markdown("---")
                        # Generate the PDF report
                        pdf_bytes = generate_cipher_report(number_string, pairs, decoded_text)
                        
                        st.download_button(
                            label="[DOWNLOAD_DATALINK_REPORT.pdf]",
                            data=pdf_bytes,
                            file_name="cipher_report.pdf",
                            mime="application/pdf",
                            type="primary",
                            use_container_width=True
                        )
                except Exception as e:
                    st.error(f"[SYSTEM_ERROR] DECODING FAILED: {e}")
    else:
        st.markdown("---")
        st.markdown("### `>> TERMINAL`")
        st.code('''
[SYSTEM LOG]
> AWAITING UPLOAD_SEQUENCE...
> NEURAL MATRIX: STANDBY
> BUFFER: EMPTY
> 
> INSTRUCTIONS:
> 1. SELECT DATA_STREAM VER. IMG
> 2. UPLOAD TO SECURE SERVER
> 3. INITIALIZE EXTRACT_PROTOCOL
        ''', language='bash')

def render_mirror_mode():
    st.header(">_ MIRROR HANDWRITING PROTOCOL")
    st.write("Upload mirrored dimensional text anomalies for inversion.")
    
    with st.expander(">> [ADVANCED] OCR ENGINE CONFIGURATION", expanded=False):
        tesseract_path = st.text_input(">_ LOCAL ENGINE PATH (DEFAULT SYSTEM VARS IF BLANK)", 
                                       value=r"C:\Program Files\Tesseract-OCR\tesseract.exe")
    
    with st.container():
        uploaded_file = st.file_uploader("[INPUT SPATIAL_ANOMALY...]", type=["jpg", "jpeg", "png"], key="mirror_uploader")
    
    if uploaded_file is not None:
        st.markdown("---")
        col_img, col_act = st.columns([1, 1])
        with col_img:
            st.image(uploaded_file, caption="[LOCATING_FRAGMENTS]", use_container_width=True)
        with col_act:
            st.markdown("### `>> SPATIAL ANOMALY DETECTED`")
            st.write("Distortion mapped. Awaiting inversion protocol.")
            execute_btn = st.button("RUN OCR EXTRACTION", type="primary", use_container_width=True)
            
        if execute_btn:
            st.markdown("---")
            with st.spinner(">> INVERTING SPATIAL PLANES..."):
                try:
                    if tesseract_path.strip():
                        setup_tesseract_path(tesseract_path.strip())
                    
                    image_bytes = uploaded_file.read()
                    flipped_cv_img, extracted_text = process_mirror_image(image_bytes)
                    
                    st.success("[EXTRACTION_COMPLETE] VALID TXT FOUND.")
                    
                    res_col1, res_col2 = st.columns(2)
                    with res_col1:
                        st.image(flipped_cv_img, channels="BGR", caption="[INVERTED_IMAGE_PLANE]", use_container_width=True)
                    with res_col2:
                        st.subheader(">> OCR_OUTPUT_BUFFER")
                        if extracted_text.strip():
                            st.info(f"**>> {extracted_text}**")
                        else:
                            st.warning("[WARNING] TEXT_UNDEFINED. CHECK QUALITY.")
                except Exception as e:
                    st.error(f"[SYSTEM_ERROR] PROCESSING FAILURE: {e}")
    else:
        st.markdown("---")
        st.markdown("### `>> TERMINAL`")
        st.code('''
[SYSTEM LOG]
> TRACKING MIRROR DISTORTIONS...
> OCR ENGINE: LINKED
> BUFFER: EMPTY
> 
> INSTRUCTIONS:
> 1. SELECT SPATIAL_ANOMALY VER. IMG
> 2. ADJUST SETTINGS IN ADVANCED CONFIG (IF REQ)
> 3. INITIALIZE INVERSION
        ''', language='bash')

def main():
    mode = initialize_ui()

    if mode == "[MODE: CIPHER_DECODER]":
        render_cipher_mode()
    else:
        render_mirror_mode()
        
    st.markdown("---")
    st.markdown("<p style='text-align: center; color: #00FF41; font-family: monospace; font-size: 0.8em;'>[END OF TRANSMISSION] // SANKETA_VISION_V1.0 // CONNECTION_SECURE</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
