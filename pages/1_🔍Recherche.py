import streamlit as st
import psycopg2
import base64

def connect_db():
    conn = psycopg2.connect(
        dbname="your_database_name",
        user="your_username",
        password="your_password",
        host="localhost",
        port="5432"
    )
    return conn

# Function to retrieve sites from database
def get_sites(conn):
    query = "SELECT name FROM sites"
    with conn.cursor() as cursor:
        cursor.execute(query)
        sites = [row[0] for row in cursor.fetchall()]
    return sites

# Function to retrieve formations based on selected site
def get_formations(conn, selected_site):
    query = """
    SELECT f.name
    FROM formations f
    JOIN sites s ON f.site_id = s.id
    WHERE s.name = %s
    """
    with conn.cursor() as cursor:
        cursor.execute(query, (selected_site,))
        formations = [row[0] for row in cursor.fetchall()]
    return formations

# Function to retrieve modules based on selected formation
def get_modules(conn, selected_formation):
    query = """
    SELECT m.name
    FROM modules m
    JOIN module_formation mf ON m.id = mf.module_id
    JOIN formations f ON mf.formation_id = f.id
    WHERE f.name = %s
    """
    with conn.cursor() as cursor:
        cursor.execute(query, (selected_formation,))
        modules = [row[0] for row in cursor.fetchall()]
    return modules

# Function to retrieve years based on selected module and formation
def get_years(conn, selected_module, selected_formation):
    query = """
    SELECT y.year_name
    FROM years y
    JOIN module_formation_year mfy ON y.id = mfy.year_id
    JOIN module_formation mf ON mfy.module_formation_id = mf.id
    JOIN modules m ON mf.module_id = m.id
    JOIN formations f ON mf.formation_id = f.id
    WHERE m.name = %s AND f.name = %s
    """
    with conn.cursor() as cursor:
        cursor.execute(query, (selected_module, selected_formation))
        years = [row[0] for row in cursor.fetchall()]
    return years

# Function to retrieve files based on all selected criteria
def get_files(conn, selected_site, selected_formation, selected_module, selected_year):
    query = """
    SELECT f.name, f.content, m.name AS module_name, y.year_name, s.name AS site_name, fo.name AS formation_name
    FROM files f
    JOIN sites s ON f.site_id = s.id
    JOIN modules m ON f.module_id = m.id
    JOIN formations fo ON f.formation_id = fo.id
    JOIN years y ON f.year_id = y.id
    WHERE 1=1
    """
    params = []

    if selected_site:
        query += " AND s.name = %s"
        params.append(selected_site)

    if selected_formation:
        query += " AND fo.name = %s"
        params.append(selected_formation)

    if selected_module:
        query += " AND m.name = %s"
        params.append(selected_module)

    if selected_year:
        query += " AND y.year_name = %s"
        params.append(selected_year)

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

    st.sidebar.markdown("### Enregistrement")
    st.sidebar.markdown("[🌍 Site](pages/2_🌍Site.py)")
    st.sidebar.markdown("[💻 Formation](pages/2_💻Formation.py)")
    st.sidebar.markdown("[📚 Modules](pages/3_📚Modules.py)")
    st.sidebar.markdown("[📆 Années](pages/4_📆Années.py)")
    st.sidebar.markdown("[📂 Mes Fichiers](pages/0_📂Mes Fichiers.py)")

    st.sidebar.markdown("### Outils et reports")
    st.sidebar.markdown("[📂 Analyser les fichiers](pages/5_📂Analyser les fichiers.py)")
    st.sidebar.markdown("[📈 Dashboard](pages/Dashboard.py)")

    st.title("🔍 Recherche Dynamique")

    st.markdown("<h3 class='text-left'>Site</h3>", unsafe_allow_html=True)
    sites = [""] + get_sites(conn)
    selected_site = st.selectbox("Site", sites, help="Choisissez un site")

    st.markdown("<h3 class='text-left'>Formation</h3>", unsafe_allow_html=True)
    formations = [""] if selected_site == "" else [""] + get_formations(conn, selected_site)
    selected_formation = st.selectbox("Formation", formations, help="Choisissez une formation")

    st.markdown("<h3 class='text-left'>Module</h3>", unsafe_allow_html=True)
    modules = [""] if selected_formation == "" else [""] + get_modules(conn, selected_formation)
    selected_module = st.selectbox("Module", modules, help="Choisissez un module")

    st.markdown("<h3 class='text-left'>Année</h3>", unsafe_allow_html=True)
    years = [""] if selected_module == "" or selected_formation == "" else [""] + get_years(conn, selected_module, selected_formation)
    selected_year = st.selectbox("Année", years, help="Choisissez une année")

    if st.button("Rechercher tous les fichiers"):
        with st.spinner('Veuillez patienter...'):
            files = get_files(conn, selected_site, selected_formation, selected_module, selected_year)

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
