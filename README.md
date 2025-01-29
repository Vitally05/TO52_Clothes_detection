# Projet de Recherche de Vêtements Similaires par Image

Ce projet a pour but de créer un programme capable de trouver des vêtements similaires à partir d'une image, avec éventuellement des options supplémentaires sous forme de texte. L'idée est simple : tu télécharges une image de vêtement, et le programme te renvoie des articles similaires en tenant compte de critères comme le type, le style ou même la matière du vêtement. En prime, tu peux aussi préciser des filtres comme la marque ou la taille !

## Fonctionnalités principales du programme

### Recherche d'images similaires
Le programme peut analyser des images de vêtements et identifier des articles similaires à partir d'une base de données d'images de vêtements.

### Critères supplémentaires 
Tu peux aussi ajouter des critères comme la marque ou la taille pour affiner les résultats de recherche.

### Interface utilisateur
Une interface simple permet d’envoyer l’image et les critères associés (texte), puis d’afficher les résultats visuellement dans un ordre de pertinence.

## Les caractéristiques du projet

### Interface utilisateur
L'interface permet aux utilisateurs de télécharger une image et d'ajouter des options de recherche sous forme de texte. L'interface affiche ensuite les résultats, en respectant l'ordre de pertinence et les critères spécifiés.

### Base de données
Le programme interagit avec une base de données contenant une grande variété de vêtements, pour pouvoir trouver des éléments similaires efficacement.

### Algorithme d'apprentissage
Un modèle a été entrainé pour reconnaître les différentes catégories de vêtements. Ensuite, un script va venir récupérer les caractéristiques de l'images téléchargée pour les comparer avec les images de vêtements de même catégorie présentes dans la base de données, en tenant compte des critères supplémentaires comme la couleur, la matière ou le style.

## Objectif final

L’objectif final serait de connecter ce programme à une plateforme comme Vinted. En intégrant cette fonctionnalité, les utilisateurs pourraient découvrir des articles en vente qui correspondent à leurs préférences exactes, rendant la recherche et l'achat de vêtements plus simples.

Cependant, cette intégration à Vinted n'a pas été réalisée dans le cadre de ce projet, notamment pour les difficulités d'accès aux données de vêtements actuellement en vente sur l'application, mais pourrait faire l’objet d’un travail futur.