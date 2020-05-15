# Utilisez les données publiques de l'Open Food Facts

## Objectifs

Créer un programme qui interagit avec la base de données pour retrouver des aliments et proposer un substitut avec un score nutritionnel plus élevé.
A travers ce programme on cherchera tout particulièrement à :
* Sélectionner les langages de programmation adaptés
* Travailler en respectant une méthodologie de projet Agile
* Implémenter le schéma de données dans la base
* Respecter les bonnes pratiques de développement en vigueur

## Cahier des charges

### Description du parcours utilisateur

Le terminal affiche les choix suivants :

1. Substituer un aliment

* Sélectionnez la catégorie. [Plusieurs propositions. L'utilisateur entre le chiffre correspondant et appuie sur entrée]
* Sélectionnez l'aliment.
[Plusieurs propositions. L'utilisateur entre le chiffre correspondant à l'aliment choisi et appuie sur entrée]
* Le programme propose un substitut, sa description, un magasin où l'acheter (le cas échéant) et un lien vers la page d'Open Food Facts concernant cet aliment.
* L'utilisateur a alors la possibilité d'enregistrer le résultat dans la base de données.

2. Afficher les aliments substitués


 

### Fonctionnalités
* Recherche d'aliments dans la base Open Food Facts.
* L'utilisateur interagit avec le programme dans le terminal, mais si vous souhaitez développer une interface graphique vous pouvez,
* Si l'utilisateur entre un caractère qui n'est pas un chiffre, le programme doit lui répéter la question,
* La recherche doit s'effectuer sur une base MySql.

## Étapes recommandés

### 1. Organiser son travail
* Découper votre programme en user stories, puis en tâches et sous-tâches.
* Github et premier push
* Écrire la documentation
### 2. Construire la base de données
* Schéma de la base de donnée
* Analyse des données de l'API Open Food Facts
* Créer la base de donnée
* Script d'initialisation de la BDD
### 3. Construire le programme
* Lister les fonctionnalités
* Construisez l'architecture
### 4. Interagir avec la BDD
* Système de question réponse
* Recherche dans la base de donnée
* Enregistrement des données


## Livrables

* Modèle physique de données et utilisant l’outil informatique de votre choix.
* Script de création de votre base de données.
* Code source publié sur Github https://github.com/Julien-V/P5/
* Tableau Trello. https://trello.com/b/XfkxWHrN/projet-5
* Document texte expliquant la démarche choisie, les difficultés rencontrées et les solutions trouvées.



## Installation et lancement

Installation
```
virtualenv Project5
cp -R P5 Project5
cd Project5
source bin/activate
pip install -r requirements.txt
```
Lancement
```
python3 main.py
```


* Testé sous Debian avec Python 3.7.6

