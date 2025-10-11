import streamlit as st
import pytesseract
from PIL import Image
import pandas as pd

st.title("Extrator de Tabela de Imagem")

uploaded_file = st.file_uploader("Envie o print da planilha", type=["png", "jpg", "jpeg"])
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Imagem enviada", use_column_width=True)

    raw_text = pytesseract.image_to_string(image)

    linhas = raw_text.strip().split("\n")
    dados = [linha.split() for linha in linhas if linha.strip()]

    df = pd.DataFrame(dados)

    st.subheader("Tabela extraída (copie e cole livremente):")
    st.dataframe(df, use_container_width=True)
