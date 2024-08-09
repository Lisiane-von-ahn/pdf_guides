import streamlit as st
from postgres import get_sites, get_formations, get_modules, add_module, delete_module

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

st.title("Gérer les Modules")

modules = get_modules()

selected_module = st.selectbox("Sélectionnez un module à supprimer", modules, index=0)
if st.button("Supprimer Module"):
    delete_module()
    st.success(f"Le module '{selected_module}' a été supprimé avec succès!")

st.markdown("---")
st.header("Ajouter un Nouveau Module")

new_module = st.text_input("Nouveau Module")
if st.button("Ajouter Module"):
    if new_module:
        add_module(new_module)
        st.success(f"Le module '{new_module}' a été ajouté avec succès!")
    else:
        st.warning("Veuillez saisir un nom de module.")
