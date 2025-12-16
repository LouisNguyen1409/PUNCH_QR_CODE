import streamlit as st
import base64
from qr_scanner_component import qr_scanner

# Page Config
st.set_page_config(page_title="QR Code Matcher", page_icon="🔍")

# CSS
st.markdown("""
    <style>
    .big-font { font-size:30px !important; font-weight: bold; text-align: center; }
    .success-text { color: green; font-size: 50px; font-weight: bold; text-align: center; }
    .error-text { color: red; font-size: 50px; font-weight: bold; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# Helper: Play Audio
def autoplay_audio(file_path: str):
    try:
        with open(file_path, "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            md = f"""
                <audio autoplay>
                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                </audio>
                """
            st.markdown(md, unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning(f"Audio file not found: {file_path}")

# State Management
if 'step' not in st.session_state:
    st.session_state.step = 0
if 'scan_result_1' not in st.session_state:
    st.session_state.scan_result_1 = None
if 'scan_result_2' not in st.session_state:
    st.session_state.scan_result_2 = None

def reset_app():
    st.session_state.step = 0
    st.session_state.scan_result_1 = None
    st.session_state.scan_result_2 = None
    st.rerun()

# --- STEP 0: Welcome ---
if st.session_state.step == 0:
    st.title("QR Code Matcher 🔍")
    st.markdown("<p class='big-font'>Ready to scan?</p>", unsafe_allow_html=True)
    
    if st.button("Start Scanning", use_container_width=True):
        st.session_state.step = 1
        st.rerun()

# --- STEP 1: Scan Sheet ---
elif st.session_state.step == 1:
    st.title("Step 1: Scan Sheet QR")
    st.info("Point camera at the QR code on the SHEET.")

    # Call the custom component
    code = qr_scanner(key="scanner_1")
    
    if code:
        st.session_state.scan_result_1 = code
        st.success(f"Captured: {code}")
        st.session_state.step = 2
        st.rerun()

# --- STEP 2: Scan Tool Box ---
elif st.session_state.step == 2:
    st.title("Step 2: Scan Tool Box QR")
    st.info("Point camera at the QR code on the TOOL BOX.")
    st.write(f"**Sheet QR:** {st.session_state.scan_result_1}")

    code = qr_scanner(key="scanner_2")

    if code:
        st.session_state.scan_result_2 = code
        st.success(f"Captured: {code}")
        st.session_state.step = 3
        st.rerun()

# --- STEP 3: Result ---
elif st.session_state.step == 3:
    st.title("Result")
    
    code1 = str(st.session_state.scan_result_1).strip()
    code2 = str(st.session_state.scan_result_2).strip()
    
    match = code1 == code2
    
    if match:
        st.markdown("<div class='success-text'>OK ✅</div>", unsafe_allow_html=True)
        st.markdown(f"<p class='big-font'>Matched: {code1}</p>", unsafe_allow_html=True)
        autoplay_audio("ok.mp3")
    else:
        st.markdown("<div class='error-text'>SAI ❌</div>", unsafe_allow_html=True)
        st.write(f"Sheet: {code1}")
        st.write(f"Tool: {code2}")
        autoplay_audio("sai.mp3")

    st.markdown("---")
    if st.button("Scan Next Pair", use_container_width=True):
        reset_app()