import os
import streamlit as st
from streamlit_pdf_viewer import pdf_viewer
from util.util import afficher_accordion, convertir_pdf_en_docx
from pdf2docx import Converter
import glob


st.title("📂Convertir PDF en DOCX")
def convertir_pdf_en_docx(chemin_pdf, chemin_docx):
    try:
        cv = Converter(chemin_pdf)
        cv.convert(chemin_docx)
        cv.close()
        print(f"Conversion réussie : {chemin_pdf} -> {chemin_docx}")
    except Exception as e:
        print(f"Erreur lors de la conversion de {chemin_pdf} en {chemin_docx}: {e}")

# Fonction pour créer le dossier kitapprenant_docx et convertir les fichiers
def organiser_et_convertir_fichiers(dossier_pdf):
    # Créer le dossier kitapprenant_docx
    dossier_kitapprenant_docx = os.path.join(dossier_pdf, "kitapprenant_docx")
    os.makedirs(dossier_kitapprenant_docx, exist_ok=True)
    
    # Trouver tous les fichiers PDF dans le dossier racine et ses sous-dossiers
    fichiers_pdf = glob.glob(os.path.join(dossier_pdf, "**/*.pdf"), recursive=True)

    for fichier_pdf in fichiers_pdf:
        # Créer le chemin du fichier DOCX correspondant dans le nouveau dossier
        nom_fichier = os.path.splitext(os.path.basename(fichier_pdf))[0] + ".docx"
        chemin_docx = os.path.join(dossier_kitapprenant_docx, nom_fichier)
        
        # Convertir le PDF en DOCX
        convertir_pdf_en_docx(fichier_pdf, chemin_docx)

# Définir le chemin de base des fichiers PDF
chemin_pdf = r''

# Organiser les fichiers et les convertir
organiser_et_convertir_fichiers(chemin_pdf)