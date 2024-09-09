import streamlit as st
import connection
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="Dashboard",
    page_icon="📊",
    layout="wide",
)
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

def get_data(query):
    with connection.get_connection() as conn:
        return pd.read_sql_query(query, conn)

sites_data = get_data("SELECT * FROM sites")
formations_data = get_data("SELECT * FROM formations")
modules_data = get_data("SELECT distinct module_id, formation_id, formations.name as name FROM files,modules, formations where files.module_id = module_id and files.formation_id = formations.id")
years_data = get_data("SELECT DISTINCT year_name FROM years")
files_data = get_data("SELECT count(1) c FROM files")

count_sites = len(sites_data)
count_formations = len(formations_data)
count_modules = len(modules_data)
count_years = len(years_data)
count_files = files_data["c"]

# Calculate file sizes
def get_file_sizes():
    with connection.get_connection()  as conn:
        c = conn.cursor()
        c.execute("SELECT name, length(file) as size FROM files")
        file_sizes = c.fetchall()
    
    file_sizes_mb = []
    for file_name, size_bytes in file_sizes:
        size_mb = size_bytes / (1024 * 1024)  # Convert bytes to MB
        file_sizes_mb.append((file_name, size_mb))
    return pd.DataFrame(file_sizes_mb, columns=['file_name', 'size_mb'])

file_sizes_data = get_file_sizes()
total_size_mb = file_sizes_data['size_mb'].sum()

st.title("📊 Dashboard des Modules")

st.markdown("## Statistiques Globales")
col1, col2, col3, col4, col5, col6 = st.columns(6)
col1.metric("Sites", count_sites)
col2.metric("Formations", count_formations)
col3.metric("Modules", count_modules)
col4.metric("Années", count_years)
col5.metric("Fichiers", count_files)
col6.metric("Taille Totale des Fichiers (MB)", f"{total_size_mb:.2f}")

st.markdown("## Nombre de Modules par Formation")
modules_per_formation = modules_data['formation_id'].value_counts().reset_index()
modules_per_formation.columns = ['formation_id', 'count']
modules_per_formation = modules_per_formation.merge(formations_data, left_on='formation_id', right_on='id')

fig1, ax1 = plt.subplots()
sns.barplot(data=modules_per_formation, x='name', y='count', ax=ax1)
ax1.set_title('Nombre de Modules par Formation')
ax1.set_xlabel('Formation')
ax1.set_ylabel('Nombre de Modules')
ax1.tick_params(axis='x', rotation=90)
st.pyplot(fig1)