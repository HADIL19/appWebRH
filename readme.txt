Système d'Information pour la Gestion des Ressources Humaines (RH)

Introduction

Ce projet est une application web conçue pour centraliser, automatiser et sécuriser les processus de gestion des ressources humaines (RH) au sein d'une entreprise. Il offre des fonctionnalités complètes pour la gestion du personnel, des congés, des salaires, des contrats, des évaluations et bien plus encore.


Objectifs

- Centraliser les données RH pour un accès rapide et sécurisé.
- Automatiser les processus RH pour réduire les tâches administratives répétitives.
- Fournir des tableaux de bord et des outils de reporting pour une meilleure visualisation et prise de décision.

Fonctionnalités Clés

1. Gestion du personnel : ajout, modification, suppression des employés, etc.
2. Gestion des congés : suivi des demandes, validation, calcul automatique des soldes, etc.
3. Gestion des salaires : calcul des salaires nets, suivi des avances, primes, absences, etc.
4. Gestion des contrats : création et suivi des contrats (CDI, CDD, stages, etc.).
5. Gestion des formations : organisation et suivi des sessions de formation.
6. Évaluations des employés : enregistrement des scores et des commentaires.
7. Offres d’emploi : publication d’offres et gestion des candidatures.
8. Gestion des services et pointages : suivi des présences et absences.

Architecture Technique

- Framework Backend : Django 5.1.4
- Langage : Python 3.13.0
- Base de données : SQLite3
- Front-end : Utilisation des templates Django avec HTML, le framework Bootstrap, JS et CSS pour la mise en page.

Installation et Configuration

Prérequis

- Python 3.13.0
- Pip (gestionnaire de packages Python)
- Environnement virtuel Python (recommandé)

Installation
. Créez un environnement virtuel et activez-le :

   bash
   python -m venv env-projet
   source env-projet/bin/activate # Linux/Mac
   env-projet\Scripts\activate   # Windows
   

. Installez Django et les dépendances requises :

   bash
   pip install django python-dateutil
   

Fichiers et Configuration

Fichier `settings.py`

python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'appRH',
]


Initialisation de la base de données

Exécutez les commandes suivantes pour configurer la base de données :

bash
python manage.py makemigrations
python manage.py migrate


Lancer le serveur de développement

bash
python manage.py runserver


Accédez à l'application via http://127.0.0.1:8000/.

Bibliothèques Utilisées

Voici les bibliothèques Python essentielles pour ce projet, accompagnées de leur utilisation :

- Django (5.1.4) : Framework web principal utilisé pour le développement du backend, la gestion de la base de données et le rendu des templates HTML.
- python-dateutil (2.9.0.post0) : Fournit des fonctionnalités avancées pour manipuler les dates, par exemple, pour calculer automatiquement les soldes des congés.
- asgiref (3.8.1) : Nécessaire pour gérer les fonctionnalités asynchrones dans Django.
- sqlparse (0.5.3) : Utilisé par Django pour analyser les requêtes SQL lors de la migration et de l'exécution de la base de données.
- tzdata (2024.2) : Fournit des données de fuseau horaire pour s'assurer que toutes les opérations liées au temps respectent les fuseaux horaires définis.
- six (1.17.0) : Une bibliothèque de compatibilité entre Python 2 et 3, utilisée par d'autres dépendances pour garantir une interopérabilité fluide.

Ces bibliothèques peuvent être installées via pip avec la commande :

bash
pip install -r requirements.txt

Modèles de Données

Modèle `Employe`

- Gère les informations personnelles des employés.
- Relation avec l'utilisateur (User).
- Champs : nom, prénom, email, téléphone, adresse, etc.

Modèle `Conge`

- Gère les demandes de congés.
- Calcul automatique des jours utilisés et mise à jour des soldes.

Modèle `Salaire`

- Gère les informations salariales des employés.
- Calcul des retenues et du salaire net.

Autres Modèles

- `Contrat` : Gère les contrats des employés.
- `Service` : Définit les services de l’entreprise.
- `Formation` : Organise les sessions de formation.
- `Evaluation` : Gère les évaluations des employés.
- `OffreEmploi`, `Candidat`, `Entretien` : Gèrent les processus de recrutement.
- `Pointage` : Suit les présences et absences.

Interface Utilisateur

L'application offre une interface intuitive avec un menu pour accéder aux fonctionnalités principales :

- Dashboard
- Gestion des employés
- Gestion des congés
- Gestion des salaires
- Et bien plus encore...

Améliorations Futures

- Intégration d'une base de données PostgreSQL pour plus de performance.
- Amélioration de l'interface utilisateur avec des frameworks comme React ou Vue.js.
- Intégration d'API REST pour une interopérabilité avec d'autres systèmes.
