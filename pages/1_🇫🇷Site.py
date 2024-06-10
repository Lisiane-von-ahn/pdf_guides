import streamlit as st
from db import get_sites, add_site, delete_site

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
