import streamlit as st
from postgres import get_sites, get_formations, get_modules, get_years, add_year, delete_year

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

st.title("Gérer les Années")

years = get_years()

selected_year = st.selectbox("Sélectionnez une année à supprimer", years, index=0)

if st.button("Supprimer"):
    delete_year()
    st.success(f"L'année '{selected_year}' a été supprimée avec succès!")

st.markdown("---")
st.header("Ajouter une Nouvelle Année")

new_year = st.text_input("Nouvelle Année")
if st.button("Ajouter"):
    if new_year:
        add_year(new_year)
        st.success(f"L'année '{new_year}' a été ajoutée avec succès!")
    else:
        st.warning("Veuillez saisir une année.")
