import streamlit as st
from postgres import get_years, duplicate_year

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
st.sidebar.page_link("pages/Cloner_annee.py", label="📆 Cloner Années")

st.title("Cloner une Année")

years = get_years()

source_year = st.selectbox("Année Source", years, help="Choisissez l'année à dupliquer")
dest_year = st.selectbox("Année Destination", years + [""], index=len(years), help="Choisissez l'année de destination ou saisissez une nouvelle année")

if st.button("Dupliquer"):
    if source_year and dest_year:
        if source_year != dest_year:
            duplicate_year(source_year, dest_year)
            st.success(f"L'année '{source_year}' a été dupliquée vers '{dest_year}' avec succès!")
        else:
            st.warning("L'année source et l'année de destination ne peuvent pas être identiques.")
    else:
        st.warning("Veuillez sélectionner ou saisir une année de destination.")

st.markdown("---")
st.info("Utilisez cette page pour dupliquer les données de fichiers d'une année existante vers une autre année.")
