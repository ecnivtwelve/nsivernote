## Cahier des charges

### UI
- [x] Implémentation de l'interface graphique
- [x] Changements de page

##  Base de données
- [x] Se connnecter
- [x] Créer un compte
- [x] Modifier les données de profil
- [ ] Ajouter une photo de profil (?)

## Développement

### Semaine 1
#### 18 mars 2024
- Exploration du projet
- Intégration de l'interface graphique.	
    - Utilisation de la librairie web `eel` (pont Python asynchrone avec JavaScript) pour l'affichage
    - Coté JavaScript, utilisation de `Alpine` pour la gestion des données en cache et de leur mise à jour sur le DOM

### Semaine 2
#### 25 mars 2024
- Ajout de la connexion utilisateur via la base de données
    - Intégration de la base de données open-source asynchrone `supabase` (sur des serveurs distants hébergés par Supabase)
    - Utilisation de `jsonpickle` pour encoder / décoder les données au format JSON.
- Ajout de la création de profil

### Semaine 3
- *(rien)*

### Semaine 4
#### 8 avril 2024
- Ajout de la récupération des cookies de connexion 
    - Utilisation de Supabase pour le login / signup managé par la base de données

#### 10 avril 2024
- Passage de la classe User et des interactions BDD en POO (classe `User`)
    - Fonctions de connexion / création de compte
    - Fonction de récupération et modification des données
- Ajout de la récupération des données de profil (utilisateur, avatar...)
- Ajout de la modification des données de profil


### Semaine 5
#### 15 avril 2024
- Commentaires du code Python
- Interface graphique de la page d'accueil
    - Menu sur le côté (repli si écran trop peu large)
    - Icônes et textes
    - Changements d'onglets
    - Boutons dynamiques

### Semaine 6
- *(rien)*

### Semaine 7
#### 05 mai 2024
- Améliorations sur l'interface graphique
    - Ajout des modals de changement de nom
    - Intégration de l'affichage des listes (avec icônes et boutons)
- Fix de l'inscription sur la base de données (ça marchait plus)
    - Problème : clés primaires qui empêchaient la création de compte sur la BDD Supabase
- Ajout des listes (récupération depuis BDD)

### Semaine 8
#### 06 mai 2024
- Réparation de bugs de connexion liés à Supabase
- Amélioration de l'interface graphique
- Nouveau nom et charte visuelle (création du logo, etc...)

### Semaine 9
#### 13 mai 2024
- Ajout des boîtes de dialogue pour créer une liste
- Ajout de la gestion complète des listes (création, renommage, suppression)
- Amélioration de l'interface (chargements, toasts, etc...)
- Fix d'un bug avec le scroll vertical sur l'interface
- Ajout d'un grand nombre d'animations sur l'interface

#### 18 mai 2024
- Ajout de l'interface des listes
- Création, édition et suppression de tâches
- Bugs mineurs corrigés