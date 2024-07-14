import streamlit as st
import psycopg2
import base64
import connection

# Database connection function
def connect_db():
    return connection.get_connection()

# Function to retrieve modules from database
def get_modules(conn):
    query = "SELECT name FROM modules order by name"
    with conn.cursor() as cursor:
        cursor.execute(query)
        modules = [row[0] for row in cursor.fetchall()]
    return modules

# Function to retrieve formations based on selected module
def get_formations(conn, selected_module):
    query = """
    SELECT f.name
    FROM formations f
    JOIN module_formation mf ON f.id = mf.formation_id
    JOIN modules m ON mf.module_id = m.id
    WHERE m.name = %s
    order by f.name
    """
    with conn.cursor() as cursor:
        cursor.execute(query, (selected_module,))
        formations = [row[0] for row in cursor.fetchall()]
    return formations

# Function to retrieve years based on selected module and formation
def get_years(conn, selected_module, selected_formation):
    query = """
    SELECT y.year_name
    FROM years y
    JOIN module_formation_year mfy ON y.id = mfy.year_id
    JOIN modules m ON mfy.module_id = m.id
    JOIN formations f ON mfy.formation_id = f.id
    WHERE m.name = %s AND f.name = %s
    order by f.name
    """
    with conn.cursor() as cursor:
        cursor.execute(query, (selected_module, selected_formation))
        years = [row[0] for row in cursor.fetchall()]
    return years

# Function to retrieve sites based on selected module, formation, and year
def get_sites(conn, selected_module, selected_formation, selected_year):
    query = """
    SELECT s.name
    FROM sites s
    JOIN module_formation_year_site mfs ON s.id = mfs.site_id
    JOIN formations f ON f.id = mfs.formation_id
    JOIN years y ON mfs.year_id = y.id
    JOIN modules m ON m.id = mfs.module_id
    WHERE m.name = %s AND f.name = %s AND y.year_name = %s
    order by s.name
    """

    print(query)

    with conn.cursor() as cursor:
        cursor.execute(query, (selected_module, selected_formation, selected_year))
        sites = [row[0] for row in cursor.fetchall()]
    return sites

# Function to retrieve files based on all selected criteria
def get_files(conn, selected_module, selected_formation, selected_year, selected_site):
    query = """
    SELECT f.name, f.file as content, m.name AS module_name, y.year_name, s.name AS site_name, fo.name AS formation_name
    FROM files f
    JOIN sites s ON f.site_id = s.id
    JOIN modules m ON f.module_id = m.id
    JOIN formations fo ON f.formation_id = fo.id
    JOIN years y ON f.year_id = y.id
    WHERE 1=1
    """
    params = []

    if selected_module:
        query += " AND m.name = %s"
        params.append(selected_module)

    if selected_formation:
        query += " AND fo.name = %s"
        params.append(selected_formation)

    if selected_year:
        query += " AND y.year_name = %s"
        params.append(selected_year)

    if selected_site:
        query += " AND s.name = %s"
        params.append(selected_site)

    query += "order by f.name"

    with conn.cursor() as cursor:
        cursor.execute(query, params)
        files = cursor.fetchall()

    return files

# Function to generate download link for a file
def generate_download_link(file_name, file_content):
    b64 = base64.b64encode(file_content).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="{file_name}" class="btn btn-primary">Télécharger</a>'
    return href

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
