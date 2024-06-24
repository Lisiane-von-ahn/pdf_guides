import streamlit as st
from db import get_sites, get_formations, add_site, add_formation, delete_site, delete_formation

logo_path = "https://le-campus-numerique.fr/wp-content/uploads/2020/12/logo-campus-header-300x60.png"  
st.sidebar.image(logo_path, use_column_width=True)

st.title("Gérer les Formations")

sites = get_sites()

# Select site for which to manage formations
selected_site_for_formations = st.selectbox("Sélectionnez un site pour afficher les formations", sites, index=0)
formations = get_formations(selected_site_for_formations)

selected_formation = st.selectbox("Sélectionnez une formation à supprimer", formations, index=0)
if st.button("Supprimer Formation"):
    delete_formation(selected_formation, selected_site_for_formations)
    st.success(f"La formation '{selected_formation}' a été supprimée avec succès!")

st.markdown("---")
st.header("Ajouter une Nouvelle Formation")

new_formation = st.text_input("Nouvelle Formation")
if st.button("Ajouter Formation"):
    if new_formation:
        add_formation(new_formation, selected_site_for_formations)
        st.success(f"La formation '{new_formation}' a été ajoutée avec succès!")
    else:
        st.warning("Veuillez saisir un nom de formation.")
