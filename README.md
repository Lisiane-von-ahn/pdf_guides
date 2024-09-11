# Application de Recherche Dynamique

Cette application Streamlit permet aux utilisateurs de rechercher et d'afficher dynamiquement des informations depuis une base de données PostgreSQL. L'application permet de sélectionner des sites, formations, modules et années, et de rechercher du texte dans les fichiers.

## Architecture 3-tiers

![Gestion de Docs]([https://github.com/username/repository/raw/main/path/to/image.png](https://github.com/Lisiane-von-ahn/pdf_guides/blob/main/architecture.jpg))

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

## Déploiement sur Streamlit Cloud

L'application peut être déployée sur Streamlit Cloud pour un accès en ligne facile. Suivez ces étapes pour déployer votre application :

- Créer un Compte Streamlit: Si vous n'avez pas encore de compte, inscrivez-vous sur Streamlit Cloud.

- Connecter votre Dépôt GitHub: Une fois connecté, connectez votre dépôt GitHub contenant votre application Streamlit.

- Déployer l'Application:
     Sur votre tableau de bord Streamlit Cloud, cliquez sur "New App".
     Sélectionnez le dépôt GitHub où se trouve votre projet.
     Choisissez la branche (généralement main) et spécifiez le fichier de démarrage (Home.py).
     Cliquez sur "Deploy" pour déployer votre application.

- Configurer les Variables d'Environnement:
     Ajoutez les variables d'environnement nécessaires, telles que les informations de connexion à votre base de données PostgreSQL, via l'interface de Streamlit Cloud.

Une fois déployée, votre application sera accessible via une URL unique fournie par Streamlit Cloud.
Utilisation

### Sélection des Paramètres

Les utilisateurs peuvent sélectionner un site, une formation, un module et une année à partir des menus déroulants disponibles. Les options disponibles sont dynamiquement filtrées en fonction des sélections précédentes.

### Recherche de Texte

Saisissez du texte dans la barre de recherche pour rechercher dans les fichiers associés à la sélection courante.

### Affichage des Résultats

Les résultats de la recherche sont affichés dans une table. Les utilisateurs peuvent télécharger les fichiers directement depuis l'interface.

## Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.

