import streamlit as st
from postgres import get_sites, get_formations, add_site, add_formation, delete_site, delete_formation

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

st.title("Gérer les Formations")

formations = get_formations()

selected_formation = st.selectbox("Sélectionnez une formation à supprimer", formations, index=0)
if st.button("Supprimer Formation"):
    delete_formation(selected_formation)
    st.success(f"La formation '{selected_formation}' a été supprimée avec succès!")

st.markdown("---")
st.header("Ajouter une Nouvelle Formation")

new_formation = st.text_input("Nouvelle Formation")
if st.button("Ajouter Formation"):
    if new_formation:
        add_formation(new_formation)
        st.success(f"La formation '{new_formation}' a été ajoutée avec succès!")
    else:
        st.warning("Veuillez saisir un nom de formation.")
