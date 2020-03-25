My Dietetic Challenge - OpenClassrooms Projet 13

Ce projet est destiné aux personnes en quête de perte de poids.
Et plus précisement aux personnes dont les connaissances 
hygièno-diététiques sont acquises mais qui manque de conseils
pour les mettre place.
Il a également pour but d'entretenir la motivation de l'utilisateur
en lui proposant, chaque semaine, un nouveau challenge adapté
à son profile.

Il fonctionne de la façon suivante :
- l'utilisateur crée son compte, il a accès au détail de son compte et à
l'onglet suivi
- dans l'onglet suivi, l'utilisateur est ammené à répondre à un questionnaire
rapide sur ces habitudes alimentaires et de vie, puis indique son objectif de poids
- lorsque l'utilisateur à validé son questionnaire, les instructions de démarrage 
du programme s'affiche ainsi que le premier challenge.
L'utilisateur a également accès à deux onglets supplémentaires : une page indiquant 
le détail de ses résultats et une autre affichant un programme alimentaire de base.
- chaque semaine l'utilisateur est invité à rentrer son poids dans l'onglet "suivi",
lui permettant d'accéder à un nouveau challenge et ce jusqu'à l'atteinte de son poids 
d'objectif.

Démarrage : Ces instructions vous permettrons de prendre connaissance 
des pré-requis et d’installer le projet afin de pouvoir développer et tester localement.

Pré-requis : 
    Python 3.7
    PostgreSQL : la base de données attendue est une base nommée "dietetic".

Installation :
    Créer un dossier au nom de "my_dietetic_challenge" sur votre disque
    
    Cloner le dépôt dans le dossier "my_dietetic_challenge" avec la commande :
    git clone https://github.com/CaroleSa/projet_13.git

    Installer et activer un environnement virtuel
    
    Installer les requirements avec la commande :
    pip install -r requirements.txt

Indiquer les données configurables :
    obligatoires :
        dietetic_project/__init__.py
        USER ligne 88 : nom utilisateur PostgreSQL 
        PASSWORD ligne 89 : mot de passe

Créer les tables dans la base de données grâce à la commande :
    python manage.py migrate

Insérer les données de démarrage dans la base de données :
    python manage.py loaddata data.json

Activer le serveur en local avec la commande :
    python manage.py runserver
Ce projet est accessible à cette adresse : A INDIQUER !!!

Auteur : Carole Sartori
