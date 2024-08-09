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

# Step 1: Select a site
st.header("Étape 1: Sélectionnez un Site")
sites = get_sites()
selected_site = st.selectbox("Sélectionnez une site", sites, index=0)

# Step 2: Select a formation based on the selected site
st.header("Étape 2: Sélectionnez une Formation")
formations = get_formations(selected_site)
selected_formation = st.selectbox("Sélectionnez une formation", formations, index=0)

# Step 3: Manage modules based on the selected formation
st.header("Étape 3: Gérer les Modules")

modules = get_modules(selected_formation)

selected_module = st.selectbox("Sélectionnez un module à supprimer", modules, index=0)
if st.button("Supprimer Module"):
    delete_module(selected_module, selected_formation)
    st.success(f"Le module '{selected_module}' a été supprimé avec succès!")

st.markdown("---")
st.header("Ajouter un Nouveau Module")
new_module = st.text_input("Nouveau Module")
if st.button("Ajouter Module"):
    if new_module:
        add_module(new_module, selected_formation)
        st.success(f"Le module '{new_module}' a été ajouté avec succès!")
    else:
        st.warning("Veuillez saisir un nom de module.")
