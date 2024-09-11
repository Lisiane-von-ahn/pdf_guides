# Application de Recherche Dynamique

Cette application Streamlit permet aux utilisateurs de rechercher et d'afficher dynamiquement des informations depuis une base de données PostgreSQL. L'application permet de sélectionner des sites, formations, modules et années, et de rechercher du texte dans les fichiers.

## Fonctionnalités

- **Sélection de Site**: Choisissez parmi une liste de sites disponibles.
- **Sélection de Formation**: Affiche les formations disponibles en fonction du site sélectionné.
- **Sélection de Module**: Affiche les modules disponibles en fonction de la formation sélectionnée.
- **Sélection d'Année**: Affiche les années disponibles en fonction du module sélectionné.
- **Recherche de Texte**: Permet de rechercher du texte dans les fichiers associés.
- **Affichage des Résultats**: Affiche les fichiers trouvés avec la possibilité de les télécharger.

## Installation

1. Clonez le dépôt et installez les dépendances :

   ```sh
   git clone https://github.com/Lisiane-von-ahn/pdf_guides.git
   pip install -r requirements.txt
   ```
Assurez-vous que votre base de données PostgreSQL est correctement configurée et que les informations de connexion sont correctement définies dans le secrets.toml de l'application.

2. Lancez le streamlit dans la machine local:
  
   ```sh
   streamlit run Home.py
   ```
   

