import streamlit as st
from db import get_sites, add_site, delete_site

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

st.title("Gérer les Sites")

sites = get_sites()

selected_site = st.selectbox("Sélectionnez un site à supprimer", sites, index=0)
if st.button("Supprimer"):
    delete_site(selected_site)
    st.success(f"Le site '{selected_site}' a été supprimé avec succès!")

st.markdown("---")
st.header("Ajouter un Nouveau Site")
new_site = st.text_input("Nouveau Site")
if st.button("Ajouter"):
    if new_site:
        add_site(new_site)
        st.success(f"Le site '{new_site}' a été ajouté avec succès!")
    else:
        st.warning("Veuillez saisir un nom de site.")
