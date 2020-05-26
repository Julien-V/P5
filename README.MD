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

## Livrables

* Modèle physique de données et utilisant l’outil informatique de votre choix.
* Script de création de votre base de données.
* Code source publié sur Github https://github.com/Julien-V/P5/
* Tableau Trello. https://trello.com/b/XfkxWHrN/projet-5
* Document texte expliquant la démarche choisie, les difficultés rencontrées et les solutions trouvées.



## Documentation

`main.main()`

Appelle la méthode core.App.run()

`init_db.Populate`

Récupère les produits d'une catégorie via l'API d'Open Food Facts et les insères dans la base de données

### openff/

`openff.core.App`

Class principale, gère les controllers, les views et les models

### openff/controllers

`openff.controllers.controller.Controller`

Contrôle la validité des différentes réponses utilisateur

`openff.controllers.category.Category`

Représente une catégorie, contrôle et insère dans la BDD

`openff.controllers.product.Product`

Représente un produit, contrôle et insère dans la BDD
### openff/models

`openff.models.config`

Fichier de configuration, contient les étapes et les requêtes SQL

`openff.models.db.DB`

Permet d'interagir avec la base de données
### openff/views

`openff.views.menu.MenuItem`

Class parent pour les objets de openff.views.menu_component

`openff.views.menu.menu_component.Title`

Une sous class de MenuItem pour afficher un titre

`openff.views.menu.menu_component.Prompt`

Une sous class de MenuItem pour personnaliser l'affichage du input

`openff.views.menu.menu_component.PrintList`

Une sous class de MenuItem pour afficher une liste

`openff.views.menu.menu_component.PrintLine`

Une sous class de MenuItem pour afficher une ligne

`openff.views.menu.menu_models.ChoiceList`

Cette class rassemble différents composants de openff.views.menu_component pour créer une view permettant d'afficher une liste et de sélectionner un élément de cette liste

`openff.views.menu.menu_models.PrintLineDB`

Cette class rassemble différents composants de openff.views.menu_component pour créer une view affichant le détail d'un produit ou le produit et le substitut côte à côte.



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

## Ajouter une catégorie
### Supprimer la base de données
```
DROP DATABASE openff;
```
### Ajouter la catégorie dans config.py
_Dans openff.models.config_
```python
cat = ["desserts-au-chocolat", "boissons-instantanees"]
cat.append("cereales-au-chocolat")
cat.append("pizzas")  # nouvelle catégorie
```
### Lancement du programme
```
python3 main.py
```


