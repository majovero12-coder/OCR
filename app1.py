import streamlit as st
import cv2
import numpy as np
import pytesseract
from PIL import Image

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="OCR - Reconocimiento de Texto",
    page_icon="🔍",
    layout="centered"
)

# --- ESTILOS PERSONALIZADOS ---
st.markdown("""
    <style>
    .stApp {
        background-color: #eaf6f6;
        color: #0b132b;
        font-family: 'Roboto', sans-serif;
    }

    h1 {
        color: #1c2541;
        text-align: center;
        font-weight: 800;
    }

    h2, h3 {
        color: #3a506b;
    }

    section[data-testid="stSidebar"] {
        background-color: #cce3e2;
        color: #0b132b;
    }

    div.stButton > button {
        background-color: #0b7fab;
        color: white;
        border-radius: 8px;
        padding: 0.5em 1em;
        border: none;
        transition: all 0.2s ease;
        font-weight: 600;
        font-size: 16px;
    }

    div.stButton > button:hover {
        background-color: #1282a2;
        transform: translateY(-2px);
    }

    .result-box {
        background-color: #ffffff;
        border-left: 5px solid #0b7fab;
        border-radius: 8px;
        padding: 15px;
        margin-top: 10px;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.08);
    }

    .footer {
        text-align: center;
        font-size: 14px;
        color: #3a506b;
        margin-top: 2em;
    }
    </style>
""", unsafe_allow_html=True)

# --- TÍTULO PRINCIPAL ---
st.title("🔍 Reconocimiento Óptico de Caracteres (OCR)")
st.write("Convierte texto de una imagen en texto digital utilizando visión por computadora y *pytesseract*.")
st.markdown("---")

# --- SIDEBAR ---
with st.sidebar:
    st.header("🧭 Opciones de captura")
    filtro = st.radio("Aplicar filtro:", ('Sin Filtro', 'Con Filtro (invertir colores)'))
    st.markdown("💡 El filtro puede mejorar la legibilidad del texto en algunas imágenes.")
    st.markdown("---")
    st.markdown("✨ *Desarrollado por María José Velásquez*")

# --- CAPTURA DE IMAGEN ---
st.subheader("📸 Captura una imagen con la cámara")
img_file_buffer = st.camera_input("Toma una foto para analizar el texto")

# --- PROCESAMIENTO ---
if img_file_buffer is not None:
    bytes_data = img_file_buffer.getvalue()
    cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)

    # Aplicar filtro opcional
    if filtro == 'Con Filtro (invertir colores)':
        cv2_img = cv2.bitwise_not(cv2_img)

    # Convertir a RGB para mostrar
    img_rgb = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)

    # Mostrar imagen procesada
    st.subheader("🖼️ Imagen procesada")
    st.image(img_rgb, caption="Vista previa de la imagen", use_container_width=True)

    # OCR
    st.subheader("🧠 Texto detectado")
    text = pytesseract.image_to_string(img_rgb)

    if text.strip():
        st.markdown(f'<div class="result-box"><strong>Resultado:</strong><br>{text}</div>', unsafe_allow_html=True)
        # --- OPCIÓN PARA DESCARGAR ---
        st.download_button(
            label="⬇️ Descargar texto como archivo .txt",
            data=text,
            file_name="texto_detectado.txt",
            mime="text/plain"
        )
    else:
        st.warning("⚠️ No se detectó texto. Intenta con una foto más clara o sin reflejos.")

# --- PIE DE PÁGINA ---
st.markdown('<p class="footer">💙 Proyecto de Interfaces Multimodales — Universidad EAFIT</p>', unsafe_allow_html=True)

    


    


