My Dietetic Challenge - OpenClassrooms Projet 13

Ce projet est destiné aux personnes en quête de perte de poids.
Et plus précisement aux personnes dont les connaissances 
hygièno-diététiques sont acquises mais qui manquent d'astuces
pour les mettre en place.
Il a également pour but d'entretenir la motivation de l'utilisateur
en lui proposant, chaque semaine, un nouveau challenge adapté
à son profile.

Il fonctionne de la façon suivante :
- l'utilisateur crée son compte, il a accès au détail de son compte et à
l'onglet suivi
- dans l'onglet suivi, il est amené à répondre à un questionnaire
rapide sur ses habitudes alimentaires et de vie, puis indique son objectif de poids
- lorsque l'utilisateur à validé son questionnaire, les instructions de démarrage 
du programme s'affichent ainsi que le premier challenge.
L'utilisateur a également accès à deux onglets supplémentaires : une page indiquant 
le détail de ses résultats et une autre affichant un programme alimentaire de base.
- chaque semaine l'utilisateur est invité à rentrer son poids dans l'onglet "suivi",
lui permettant d'accéder à un nouveau challenge et ce jusqu'à l'atteinte de son poids 
d'objectif.

Démarrage : Ces instructions vous permettront de prendre connaissance 
des pré-requis et d’installer le projet afin de pouvoir développer et tester localement.

Pré-requis : 
    Python 3.7
    PostgreSQL : la base de données attendue est une base nommée "dietetic".

Installation :
    Créer un dossier au nom de "my_dietetic_challenge" sur votre disque
    
    Cloner le dépôt dans le dossier "my_dietetic_challenge" avec la commande :
    git clone https://github.com/CaroleSa/projet_13.git

    Installer et activer un environnement virtuel
    
    Installer les dépendances avec la commande :
    pip install -r requirements.txt

Indiquer les données configurables :

    dietetic_project/__init__.py
        USER ligne 88 : nom utilisateur PostgreSQL 
        PASSWORD ligne 89 : mot de passe

Modifier la structure de la base de données grâce à la commande :
    python manage.py migrate

Insérer les données de démarrage dans la base de données :
    python manage.py loaddata data.json
    
Interface d'administration, créer un super-utilisateur :
    python manage.py createsuperuser
    puis suivre les indications

Activer le serveur en local avec la commande :
    python manage.py runserver
    (accès à l'interface d'administration : /admin/)
    
Ce projet est accessible à cette adresse : A INDIQUER !!!

Auteur : Carole Sartori
