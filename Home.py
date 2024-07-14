import streamlit as st
from pdf_guides.util.dbLink import connect_db,get_files, get_formations, get_modules, get_sites, get_years
from util.util import generate_download_link

# Main Streamlit code
def main():
    conn = connect_db()

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

    st.title("🔍 Recherche Dynamique")

    st.markdown("<h3 class='text-left'>Module</h3>", unsafe_allow_html=True)
    modules = [""] + get_modules(conn)
    selected_module = st.selectbox("Module", modules, help="Choisissez un module")

    st.markdown("<h3 class='text-left'>Formation</h3>", unsafe_allow_html=True)
    formations = [""] if selected_module == "" else [""] + get_formations(conn, selected_module)
    selected_formation = st.selectbox("Formation", formations, help="Choisissez une formation")

    st.markdown("<h3 class='text-left'>Année</h3>", unsafe_allow_html=True)
    years = [""] if selected_module == "" or selected_formation == "" else [""] + get_years(conn, selected_module, selected_formation)
    selected_year = st.selectbox("Année", years, help="Choisissez une année")

    st.markdown("<h3 class='text-left'>Site</h3>", unsafe_allow_html=True)
    sites = [""] if selected_module == "" or selected_formation == "" or selected_year == "" else [""] + get_sites(conn, selected_module, selected_formation, selected_year)
    selected_site = st.selectbox("Site", sites, help="Choisissez un site")

    if st.button("Rechercher tous les fichiers"):
        with st.spinner('Veuillez patienter...'):
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
                                <th>Télécharger</th>
                            </tr>
                        </thead>
                        <tbody>
                    """
                for file in files:
                    file_name, file_content, module_name, year_name, site_name, formation_name = file
                    download_link = generate_download_link(file_name, file_content)
                    html += f"<tr><td>{file_name}</td><td>{module_name}</td><td>{year_name}</td><td>{site_name}</td><td>{formation_name}</td><td>{download_link}</td></tr>"

                html += "</tbody></table>"
                st.markdown(html, unsafe_allow_html=True)
            else:
                st.warning("Aucun fichier trouvé.")

    conn.close()

if __name__ == "__main__":
    main()
