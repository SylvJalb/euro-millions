# TODO API

## Context

Training a machine learning modele on a EuroMillion win/lose combination dataset to know if a random combination of
numbers is a winning one.  
One combination : 5 numbers (between 1-50) and 2 star number (between 1-12).

## API CALL

### POST

> **POST** ***/api/predict***

Permet de réaliser une prédiction en fonction d’une proposition de tirage en entrée La prédiction devra être
probabiliste (Proba gain : X%, Proba perte : 1-X%).

> **POST** ***/api/model/retrain***

Permet de réentrainer le modèle Il doit prendre en compte les données rajoutées a posteriori

### GET

> **GET** ***/api/predict***

Permet de générer une combinaison de numéros ayant une probabilité de gain élevée. (Définir élevée selon votre
compréhension/étude de la donnée/modèle)
La prédiction d

> **GET** ***/api/model***

Permet d’obtenir les informations techniques du modèle -Métriques de performance -Nom de l’algorithme -Paramètres
d’entraînement

### PUT

> **PUT** ***/api/model***

Permet d’enrichir le modèle d’une donnée supplémentaire Une donnée supplémentaire doit avoir le même format que le reste
des données.


