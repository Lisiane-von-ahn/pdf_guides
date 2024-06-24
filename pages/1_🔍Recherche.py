import streamlit as st
import sqlite3
import base64
from io import BytesIO

logo_path = "https://le-campus-numerique.fr/wp-content/uploads/2020/12/logo-campus-header-300x60.png"  
st.sidebar.image(logo_path, use_column_width=True)

from db import (
    get_sites, get_formations, get_modules, get_years, get_files
)

def generate_download_link(file_name, file_data):
    b64 = base64.b64encode(file_data).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="{file_name}" class="btn btn-primary">Télécharger</a>'
    return href

st.markdown(
    """
    <link href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
    """,
    unsafe_allow_html=True
)

st.title("🔍 Recherche Dynamique")

st.markdown("<h3 class='text-left'>Site</h3>", unsafe_allow_html=True)
sites = [""] + get_sites()
selected_site = st.selectbox("Site", sites, help="Choisissez un site")

st.markdown("<h3 class='text-left'>Formation</h3>", unsafe_allow_html=True)
formations = [""] if selected_site == "" else [""] + get_formations(selected_site)
selected_formation = st.selectbox("Formation", formations, help="Choisissez une formation")

st.markdown("<h3 class='text-left'>Module</h3>", unsafe_allow_html=True)
modules = [""] if selected_formation == "" else [""] + get_modules(selected_formation)
selected_module = st.selectbox("Module", modules, help="Choisissez un module")

st.markdown("<h3 class='text-left'>Années</h3>", unsafe_allow_html=True)
years = [""] if selected_module == "" else [""] + get_years(selected_module)
selected_year = st.selectbox("Année", years, help="Choisissez une année")

st.markdown("<h3 class='text-left'>Rechercher Modules qui contiennent</h3>", unsafe_allow_html=True)
module_search_text = st.text_input("Rechercher Modules qui contiennent", "")

st.markdown("<h3 class='text-left'>Rechercher Filename qui contiennent</h3>", unsafe_allow_html=True)
filename_search_text = st.text_input("Rechercher Filename qui contiennent", "")

st.markdown("<h3 class='text-left'>Rechercher dans le texte du fichier</h3>", unsafe_allow_html=True)
search_text = st.text_input("Rechercher du texte dans le fichier", "")

if st.button("Rechercher tous les fichiers"):
    with st.spinner('Merci de bien vouloir patienter...'):
        files = []

        query = """
        SELECT files.file_name, files.content, modules.name AS module_name, years.year, sites.name AS site_name, formations.name AS formation_name
        FROM files
        JOIN years ON files.year_id = years.id
        JOIN modules ON years.module_id = modules.id
        JOIN formations ON modules.formation_id = formations.id
        JOIN sites ON formations.site_id = sites.id
        WHERE 1=1
        """
        
        params = []

        if selected_site:
            query += " AND sites.name LIKE ?"
            params.append(f'%{selected_site}%')
        
        if selected_formation:
            query += " AND formations.name LIKE ?"
            params.append(f'%{selected_formation}%')
        
        if selected_module:
            query += " AND modules.name LIKE ?"
            params.append(f'%{selected_module}%')
        
        if selected_year:
            query += " AND years.year LIKE ?"
            params.append(f'%{selected_year}%')

        if module_search_text:
            query += " AND modules.name LIKE ?"
            params.append(f'%{module_search_text}%')
        
        if filename_search_text:
            query += " AND files.file_name LIKE ?"
            params.append(f'%{filename_search_text}%')

        if search_text:
            query += " AND files.text_content LIKE ?"
            params.append(f'%{search_text}%')

        with sqlite3.connect('modules.db') as conn:
            c = conn.cursor()
            c.execute(query, params)
            files = c.fetchall()

        if files:
            html = f"""
                <table class='table table-dark table-striped'>
                    <thead>
                        <tr>
                            <th>Nom du fichier</th>
                            <th>Module</th>
                            <th>Année</th>
                            <th>Site</th>
                            <th>Formation</th>
                            <th>Télécharger</th>
                        </tr>
                    </thead>
                    <tbody>
                """
            for file in files:
                file_name, file_data, module_name, year, site_name, formation_name = file
                download_link = generate_download_link(file_name, file_data)

                html += f"<tr><td>{file_name}</td><td>{module_name}</td><td>{year}</td><td>{site_name}</td><td>{formation_name}</td><td>{download_link}</td></tr>"

            html += f"</tbody></table>"

            st.markdown(html, unsafe_allow_html=True)        
        else:
            st.warning("Aucun fichier trouvé.")
