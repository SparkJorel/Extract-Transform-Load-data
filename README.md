# Extract-Transform-Load-data
Ce projet consiste a extraires les informations qui sont dans differents fichier, les transformer ensuite les charger dans une base de donnees sql
# README - Gestion d’une Base de Données MySQL avec Python et XAMPP

## Introduction
Ce projet montre comment :
1. Faire des operations d'extraction et de transformation sur les donnees brutes.
2. Écrire des scripts Python pour lire des fichiers txt et CSV et insérer les données dans la base de données.
3. Utiliser le SGBD MySQL pour stocker et visualiser les données.

## Prérequis
- [XAMPP](pour MySQL et phpMyAdmin).
- Python (avec le module `mysql-connector-python` installé).
- Avoir tous les fichiers csv et dossiers de donnees dans le mm repertoire.

## Étapes du Projet

### 1. Création des Tables dans la Base de Données

#### Script SQL pour Créer les Tables

```sql
CREATE DATABASE IF NOT EXISTS bd_articles;
USE bd_articles;

-- Table Pays
CREATE TABLE pays (
    id_pays INT PRIMARY KEY AUTO_INCREMENT,
    nom_pays VARCHAR(255) NOT NULL
);

-- Table Ville
CREATE TABLE ville (
    id_ville INT PRIMARY KEY AUTO_INCREMENT,
    nom_ville VARCHAR(255) NOT NULL,
    id_pays INT NOT NULL,
    FOREIGN KEY (id_pays) REFERENCES pays(id_pays)
);

-- Table Affiliation
CREATE TABLE affiliation (
    id_affiliation INT PRIMARY KEY AUTO_INCREMENT,
    nom_affiliation VARCHAR(255) NOT NULL,
    id_ville INT NOT NULL,
    FOREIGN KEY (id_ville) REFERENCES ville(id_ville)
);

-- Table Auteur
CREATE TABLE auteur (
    id_auteur INT PRIMARY KEY AUTO_INCREMENT,
    nom_auteur VARCHAR(255) NOT NULL,
    id_affiliation INT NOT NULL,
    FOREIGN KEY (id_affiliation) REFERENCES affiliation(id_affiliation)
);

-- Table Article
CREATE TABLE article (
    id_article INT PRIMARY KEY AUTO_INCREMENT,
    titre_article VARCHAR(255) NOT NULL
);

-- Table Rediger
CREATE TABLE rediger (
    id_article INT NOT NULL,
    id_auteur INT NOT NULL,
    annee YEAR NOT NULL,
    PRIMARY KEY (id_article, id_auteur),
    FOREIGN KEY (id_article) REFERENCES article(id_article),
    FOREIGN KEY (id_auteur) REFERENCES auteur(id_auteur)
);

```

### 2. Script Python pour Insérer les Données
Le script Python effectue les actions suivantes :
1. Lire les données du fichier CSV.
2. Insère les données dans les tables correspondantes tout en gérant les relations.


### 3. Informations sur la Connexion à la Base de Données
Pour se connecter à MySQL avec XAMPP, importez d'abord la BD dans votre SGBD puis utilisez les paramètres suivants :
- **Hôte** : `localhost`
- **Utilisateur** : `root`
- **Mot de passe** : Chaîne vide (`""`)
- **Base de données** : `bd_articles`

## Conclusion
Ce projet nous permettra d'effectuer des visualisations des donnees stockes en bd afin de trouver facilement des solutions.

