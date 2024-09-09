import streamlit as st
import time  # Import the time module
from util.dbLink import connect_db, get_files, get_formations, get_modules, get_sites, get_years, get_files_by_id
from util.util import generate_download_link, extraire_liens, liensNOk, liensOk
from util.pdfmanage import convert_pdf_to_docx, generate_download_link_doc, generateTempFile
from io import BytesIO
import verifier_liens

# Main Streamlit code
def main():
    conn = connect_db()

    checkbox_liens = st.checkbox('Vérifier liens ?')

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

    st.title("🔍 Recherche Dynamique")

    st.markdown("<h3 class='text-left'>Module</h3>", unsafe_allow_html=True)
    modules = [""] + get_modules(conn)
    selected_module = st.selectbox("Module", modules, help="Choisissez un module")

    st.markdown("<h3 class='text-left'>Année</h3>", unsafe_allow_html=True)
    years = [""] + get_years(conn, selected_module, "")
    selected_year = st.multiselect("Année", years, help="Choisissez une année")

    st.markdown("<h3 class='text-left'>Formation</h3>", unsafe_allow_html=True)
    formations = [""] + get_formations(conn, selected_module)
    selected_formation = st.multiselect("Formation", formations, help="Choisissez une formation")

    st.markdown("<h3 class='text-left'>Site</h3>", unsafe_allow_html=True)
    sites = [""] + get_sites(conn, selected_module, selected_formation, selected_year)
    selected_site = st.selectbox("Site", sites, help="Choisissez un site")

    if st.button("Rechercher tous les fichiers"):
        with st.spinner('Veuillez patienter...'):
            start_time = time.time()  # Start timer

            files = get_files(conn, selected_module, selected_formation, selected_year, selected_site)

            if files:
                html = """
                    <table class='table table-dark table-striped'>
                        <thead>
                            <tr>
                                <th>Nom du fichier</th>
                                <th>Module</th>
                                <th>Année</th>
                                <th>Site</th>
                                <th>Formation</th>
                                <th>Télécharger</th>"""
                                
                if checkbox_liens:
                    html += """<th>Liens OK</th><th>Liens NOK</th><th>Liens NOK Détails</th>"""

                html += """</tr></thead><tbody>"""

                for file in files:
                    print(file)
                    id, file_name, file_content, module_name, year_name, site_name, formation_name,liens_ok,liens_nok,liens_nok_details = file
                    download_link = generate_download_link(file_name, file_content)

                    if liens_nok == None:
                        verifier_liens.process_file_by_fields(file_name,file_content,id)
                        id, file_name, file_content, module_name, year_name, site_name, formation_name,liens_ok,liens_nok,liens_nok_details = get_files_by_id(conn,id)

                    html += f"<tr><td>{file_name}</td><td>{module_name}</td><td>{year_name}</td><td>{site_name}</td><td>{formation_name}</td><td>{download_link}</td>"

                    if liens_ok == None: 
                        liens_ok = 0
                        liens_nok = 0
                        liens_nok_details = ""

                    if checkbox_liens:
                        urls = liens_nok_details.split()
                        html_links = "".join([f'<a href="{url}">{url}</a> | ' for url in urls])
                        html += f"<td>{liens_ok}</td><td>{liens_nok}</td><td>{html_links}</td>"

                    html += "</tr>"

                html += "</tbody></table>"
                st.markdown(html, unsafe_allow_html=True)
            else:
                st.warning("Aucun fichier trouvé.")

            end_time = time.time()  # End timer
            elapsed_time = end_time - start_time  # Calculate elapsed time
            st.info(f"Temps de recherche: {elapsed_time:.2f} seconds")  # Display elapsed time

    conn.close()

if __name__ == "__main__":
    main()
