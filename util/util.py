import requests
import streamlit as st
import PyPDF2
from docx import Document
from docx.oxml.ns import qn
import base64

def creer_tableau_resume(st,listeBon, listeMauvais):
    st.markdown("<b><font color=red>" + str(len(listeMauvais)) + " Lien(s) ne marche(nt) pas</font> </b>", unsafe_allow_html=True)
    
    for lien in listeMauvais:
        st.write(lien)
    
    st.markdown("<b><font color=green>" + str(len(listeBon)) + " Lien(s) marche(nt) bien</font> </b>", unsafe_allow_html=True)
    
    for lien in listeBon:
        st.write(lien)

def afficher_accordion(name, liens):
    st.write("Nom du fichier:", name)
    
    liensBons = []
    liensMauvais = []

    for lien in liens:
        if mon_lien_est_bon(lien):
            liensBons.append(lien)
        else:
            liensMauvais.append(lien)

    with st.expander("Résumé des liens"):
        creer_tableau_resume(st, liensBons, liensMauvais)
        
def liensOk(liens):
    
    liensBons = []
    liensMauvais = []

    for lien in liens:
        if mon_lien_est_bon(lien):
            liensBons.append(lien)
        else:
            liensMauvais.append(lien)

    return liensBons.count()

def liensNOk(liens):
    
    liensBons = []
    liensMauvais = []

    for lien in liens:
        if mon_lien_est_bon(lien):
            liensBons.append(lien)
        else:
            liensMauvais.append(lien)

    return len(liensMauvais)


def liensOk(liens):
    
    liensBons = []
    liensMauvais = []

    for lien in liens:
        if mon_lien_est_bon(lien):
            liensBons.append(lien)
        else:
            liensMauvais.append(lien)

    return len(liensBons)
def mon_lien_est_bon (lien):    
    try:
        response = requests.get(lien)
        response.raise_for_status()
    except requests.HTTPError as http_err:
        return False
    except Exception as err:
        return False
    else:
        return True    

def extraire_liens_dans_docx(fichier_docx):
    liens = []
    doc = Document(fichier_docx)

    for paragraph in doc.paragraphs:
        text = paragraph.text
        start = 0
        while start < len(text):
            start_index = text.find('http', start)
            if start_index == -1:
                break
            end_index = text.find(' ', start_index)
            if end_index == -1:
                end_index = len(text)
            url = text[start_index:end_index]
            liens.append(url)
            start = end_index

    return liens

def extraire_liens (fichier):
    if "docx" in fichier:
        return extraire_liens_dans_docx(fichier)
    else:
        return extraire_liens_dans_pdf(fichier)


def extraire_liens_dans_pdf(fichier_pdf):

    # c'est la clé des annotations trouvés dans le PDF, les annotations sont types d'objets comme hyperlinks    
    key = '/Annots'
    # c'est pour # specifier que je veux un hyperlink format URI/URL
    uri = '/URI'
    # ici je ne prends que les anchors (hyperlinks)
    ank = '/A'
    
    #ici c'est un array qui contient les liens qu'on va retourner
    liens = []
    
    # Ouvrir le fichier PDF avec rb qui signifie que je ne veux que lire (read) et b c'est pour normaliser le charset
    with open(fichier_pdf, 'rb') as fichier:
        # J'utilise la biblioteque pypdf2 pour ouvrir le pdf et pouvoir travailler avec lui
        lecteur = PyPDF2.PdfReader(fichier)
        
        # pour chaque page trouvée dans le document, je prends le texte et je vais chercher les liens
        for num_page in range(len(lecteur.pages)):
            page = lecteur.pages[num_page]
            pageObject = page.get_object()
            # si le type d'objet est annotation (defini dans la variable précedente) on va prendre les hyperlinks et l'uri
            if key in pageObject.keys():
                ann = pageObject[key]
                for a in ann:
                    u = a.get_object()
                    if uri in u[ank].keys():
                        mylink = u[ank][uri]
                        liens.append(mylink)

    return liens

# Function to generate download link for a file
def generate_download_link(file_name, file_content):
    b64 = base64.b64encode(file_content).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="{file_name}" class="btn btn-primary">Télécharger</a>'
    return href
