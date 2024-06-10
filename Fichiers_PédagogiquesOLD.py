import streamlit as st
import os
import pdfplumber
from streamlit_quill import st_quill
from pdfminer.high_level import extract_text
from streamlit.components.v1 import html,components
import fitz
from weasyprint import HTML


from db import (
    get_sites, get_modules, get_years, get_files, add_site, add_module,
    add_year, add_file, update_file_content, delete_site, delete_module,
    delete_year, delete_file
)

def html_to_pdf(html_content, output_path):
    HTML(string=html_content).write_pdf(output_path)

def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text += page.get_text("html")  # Get text as HTML
    return text

def extract_text_from_pdf_pdfminer(file_path):
    return extract_text(file_path)


st.markdown(
    """
    <link href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
    """,
    unsafe_allow_html=True
)

st.title("📂 Objectifs pédagogiques du module")

st.markdown("<h3 style='text-align: left;'>Site</h3>", unsafe_allow_html=True)
selected_site = st.selectbox(" ", get_sites(), help="Choisissez un site")

st.markdown("<h3 style='text-align: left;'>Module</h3>", unsafe_allow_html=True)
selected_module = st.selectbox(" ", get_modules(selected_site), help="Choisissez un module")

st.markdown("<h3 style='text-align: left;'>Années</h3>", unsafe_allow_html=True)
selected_year = st.selectbox(" ", get_years(selected_module, selected_site), help="Choisissez une année")

st.subheader(f"{selected_module} - {selected_year}")

uploaded_file = st.file_uploader("Upload File", type=["pdf"], accept_multiple_files=False)

if st.button("Lire fichier et Sauvegarder", key=f"lire") and uploaded_file:
    text = ""

    file_name = os.path.join("uploaded_files", uploaded_file.name)
    with open(file_name, "wb") as f:
        f.write(uploaded_file.getbuffer())

    with pdfplumber.open(file_name) as pdf:
        for page in pdf.pages:
            text += page.extract_text()

    text = extract_text_from_pdf_pdfminer(file_name)

    delete_file(selected_year, selected_module, selected_site)
    add_file("Kit", text, selected_year, selected_module, selected_site)

files = get_files(selected_year, selected_module, selected_site)

if files:
    quill_content = st_quill(value=files[0], html=True)

if st.button("Sauvegarder Changements", key=f"save"):
    delete_file(selected_year, selected_module, selected_site)
    add_file("Kit",quill_content, selected_year, selected_module, selected_site)


if st.button("Convert to PDF"):
    output_path = f"{selected_site}-{selected_module}-{selected_year}.pdf"
    html_to_pdf(quill_content, output_path)
    st.success("PDF Generated Successfully!")

    with open(output_path, "rb") as f:
        pdf_data = f.read()

    st.download_button(label="Download PDF", data=pdf_data, file_name=output_path, mime="application/pdf")
