import streamlit as st
from streamlit_pdf_viewer import pdf_viewer
from util.util import afficher_accordion,extraire_liens

logo_path = "https://le-campus-numerique.fr/wp-content/uploads/2020/12/logo-campus-header-300x60.png"  
st.sidebar.image(logo_path, use_column_width=True)

st.sidebar.page_link("pages/1_🔍Recherche.py", label="🔍 Recherche dynamique")

st.sidebar.caption("Enregistrement")
st.sidebar.page_link("pages/2_🌍Site.py", label="🌍 Site")
st.sidebar.page_link("pages/2_💻Formation.py", label="💻 Formation")
st.sidebar.page_link("pages/3_📚Modules.py", label="📚 Modules")
st.sidebar.page_link("pages/4_📆Années.py", label="📆 Années")
st.sidebar.page_link("pages/0_📂Mes Fichiers.py", label="📂 Mes Fichiers")

st.sidebar.caption("Outils et reports")
st.sidebar.page_link("pages/5_📂Analyser les liens .py", label="📂 Analyser Fichiers")
st.sidebar.page_link("pages/Dashboard.py", label="📈 Dashboard")
st.sidebar.caption("Automation")
st.sidebar.page_link("pages/Cloner_annee.py", label="📆 Cloner Années")

st.title("📂Analyser les liens")

# Liste pour stocker les fichiers PDF chargés
pdf_files = []

# Fonction pour afficher les fichiers PDF
def display_pdf(pdf_data):
    pdf_viewer(input=pdf_data)

checkbox_result = st.checkbox('Afficher Preview (seul pdf) ?')

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

            if checkbox_result == True and "pdf" in str(fichier_uploade.name).lower():
                display_pdf(donnees)