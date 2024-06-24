import os
import fitz
import base64
import streamlit as st
from docx import Document
from streamlit.components.v1 import html
from db import (
    get_sites, get_formations, get_modules, get_years, get_files, add_site, add_formation, add_module,
    add_year, add_file, update_file_content, delete_site, delete_formation, delete_module,
    delete_year, delete_file
)

st.markdown(
    """
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.3/dist/umd/popper.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
    """,
    unsafe_allow_html=True
)

def lire_pdf(chemin_fichier):
    try:
        doc = fitz.open(chemin_fichier)
        contenu = ""
        for page in doc:
            contenu += page.get_text()
        return contenu
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier PDF {chemin_fichier}: {e}")
        return ""

def lire_docx(chemin_fichier):
    try:
        doc = Document(chemin_fichier)
        contenu = ""
        for paragraphe in doc.paragraphs:
            contenu += paragraphe.text
        return contenu
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier DOCX {chemin_fichier}: {e}")
        return ""

def generate_download_link(file_name, file_data):
    b64 = base64.b64encode(file_data).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="{file_name}">Télécharger</a>'
    return href

def displayPdf(file_data):
    doc = fitz.open("pdf", file_data)
    page = doc.load_page(st.session_state.current_page)
    pix = page.get_pixmap()
    img = pix.tobytes("png")
    st.image(img, width=700)

st.markdown(
    """
    <link href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
    """,
    unsafe_allow_html=True
)

logo_path = "https://le-campus-numerique.fr/wp-content/uploads/2020/12/logo-campus-header-300x60.png"  
st.sidebar.image(logo_path, use_column_width=True)

st.title("📂 Objectifs pédagogiques du module")

st.markdown("<h3 style='text-align: left;'>Site</h3>", unsafe_allow_html=True)
selected_site = st.selectbox(" ", get_sites(), help="Choisissez un site")

st.markdown("<h3 style='text-align: left;'>Formation</h3>", unsafe_allow_html=True)
selected_formation = st.selectbox(" ", get_formations(selected_site), help="Choisissez une formation")

st.markdown("<h3 style='text-align: left;'>Module</h3>", unsafe_allow_html=True)
selected_module = st.selectbox(" ", get_modules(selected_formation), help="Choisissez un module")

st.markdown("<h3 style='text-align: left;'>Années</h3>", unsafe_allow_html=True)
selected_year = st.selectbox(" ", get_years(selected_module), help="Choisissez une année")

st.subheader(f"{selected_module} - {selected_year}")

uploaded_file = st.file_uploader("Upload File", type=["pdf"], accept_multiple_files=False)

if st.button("Lire fichier et Sauvegarder", key=f"lire") and uploaded_file:
    file_name = uploaded_file.name
    pdf_bytes = uploaded_file.read()

    if file_name.lower().endswith('.pdf'):
        contenu = lire_pdf(file_name)
    elif file_name.lower().endswith('.docx'):
        contenu = lire_docx(file_name)

    add_file(file_name, pdf_bytes, selected_year, selected_module, contenu)
    st.success("File uploaded and saved successfully!")

files = get_files(selected_year, selected_module)

if files:
    
    html = "<table class='table-dark'><thead class='thead-dark'><tr><th>Nom du fichier</th><th>Télécharger</th></tr></thead><tbody>"
    
    st.markdown("### Fichiers disponibles")
    
    for file in files:
        file_name = file[0]
        file_data = file[1]
        download_link = generate_download_link(file_name, file_data)
        html += f"<tr><td>{file_name}</td><td>{download_link}</td></tr>"
    
    html += "</tbody></table>"

    st.markdown(html,unsafe_allow_html=True)
