import streamlit as st
from streamlit_pdf_viewer import pdf_viewer
import base64
from util import *

st.title("📂Analyser les liens")

# Liste pour stocker les fichiers PDF chargés
pdf_files = []

# Fonction pour afficher les fichiers PDF
def display_pdf(pdf_data):
    pdf_viewer(input=pdf_data, width=700)

checkbox_result = st.checkbox('Afficher Preview ?')

# Section pour charger les fichiers
st.subheader("Télécharger des fichiers PDF ou DOCX")
fichiers_uploades = st.file_uploader("Choisissez des fichiers PDF", type=['pdf', 'docx'], accept_multiple_files=True)

# Si des fichiers ont été téléchargés
if fichiers_uploades:
    with st.spinner('En train de charger, merci de bien vouloir patienter !'):
        for fichier_uploade in fichiers_uploades:
            # Lit les données du fichier PDF
            donnees = fichier_uploade.read()
            # Ajoute les données du PDF à la liste des fichiers PDF
            pdf_files.append(donnees)

            # Save the uploaded file with the safe filename
            with open(fichier_uploade.name, 'wb') as f:
                f.write(donnees)

            # Obtenir les liens
            liens = extraire_liens(fichier_uploade.name)
            
            afficher_accordion(fichier_uploade.name,liens)        
            
            if checkbox_result == True:
                with st.expander("Preview du fichier (seul PDF)"):
                    if "pdf" in donnees:
                        display_pdf(donnees)