import streamlit as st
from db import get_sites, get_formations, get_modules, add_module, delete_module

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
