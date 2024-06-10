import os
import fitz
import streamlit as st
from streamlit.components.v1 import html
from db import (
    get_sites, get_formations, get_modules, get_years, get_files, add_site, add_formation, add_module,
    add_year, add_file, update_file_content, delete_site, delete_formation, delete_module,
    delete_year, delete_file
)

def displayPdf():
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

    delete_file(selected_year, selected_module)
    add_file(file_name, pdf_bytes, selected_year, selected_module)
    st.success("File uploaded and saved successfully!")

files = get_files(selected_year, selected_module)

if files:

    pdf_data = files[0] 

    with open("temp.pdf", "wb") as f:
        f.write(pdf_data)

    doc = fitz.open("temp.pdf")
    num_pages = doc.page_count

    try:
        if st.session_state.current_page == 0:
            st.session_state.current_page = 0
    except:
       st.session_state.current_page = 0
     
    if st.button("Page Précédente") and st.session_state.current_page > 0:
        st.session_state.current_page -= 1

    if st.button("Page Suivante") and st.session_state.current_page < num_pages - 1:
        st.session_state.current_page += 1

    displayPdf()


if st.button("Générer fichier pour télécharger"):
    output_path = f"{selected_site}-{selected_module}-{selected_year}.pdf"
    with open(output_path, "wb") as f:
        f.write(pdf_data)
    st.success("Fichier généré")

    with open(output_path, "rb") as f:
        pdf_data = f.read()

    st.download_button(label="Télécharger PDF", data=pdf_data, file_name=output_path, mime="application/pdf")

