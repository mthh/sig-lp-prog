---
title: "Module SIG - Séance 5 - 2022-2023"
author: [Matthieu Viry]
date: "2023-02-08"
linkcolor: blue
fontsize: 11pt
toc: true
header-includes: |
	\usepackage{caption}
	\captionsetup[figure]{
      name=,
      labelsep=none,
      labelformat=empty}
include-before: |
    # Séance 5 - TP - PostGIS 1
...


**Objectif** : Ce TP a pour pour but de vous familiariser avec PostGIS et avec les requêtes spatiales. Dans ce TP nous utiliserons seulement les outils fournis avec PostgreSQL / PostGIS. Il n'est en effet pas nécessaire d'utiliser un logiciel SIG de bureau pour répondre à des questions d'analyse spatiale.

## 0. Préambule - Installation de PostgreSQL et PostGIS

### 0.1 Pour Windows et si vous n'avez pas déjà PostgreSQL

\small

- Avant toute chose : installer les bibliothèques Microsoft C et C++ nécessaires (téléchargement depuis la page [https://learn.microsoft.com/fr-fr/cpp/windows/latest-supported-vc-redist?view=msvc-170](https://learn.microsoft.com/fr-fr/cpp/windows/latest-supported-vc-redist?view=msvc-170) / lien direct : [https://aka.ms/vs/17/release/vc_redist.x64.exe](https://aka.ms/vs/17/release/vc_redist.x64.exe) puis installation en exécutant le fichier téléchargé).

- Télécharger l'installeur PostgreSQL disponible à partir du site [https://www.postgresql.org/](https://www.postgresql.org/) (lien direct : [https://www.enterprisedb.com/downloads/postgres-postgresql-downloads](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads) puis sélectionner la version **14.6** pour Windows x86-64).


- Exécuter l'installeur et laisser sélectionnés les 4 composants par défaut (*Postgresl Server*, *pgadmin 4*, *Stack Builder* et *Command Line Tools*)

- Sélectionner un mot de passe pour le superutilisateur **postgres** (il est important de s'en souvenir pour la suite de ce TP et le suivant).

- Valider les différents choix proposés jusqu'à la fin de l'installation.

- L'application Stack Builder s'ouvre à la fin de l'installation (sinon ouvrez la manuellement).

- Sélectionnez la dernière version de PostGIS (3.3.2) en la sélectionnant sous l'item "Spatial Extensions".

- Validez par l'affirmative les différentes étapes / questions qui suivent.

- Une fois l'installation effectuée, vous pouvez cliquer sur "Close" pour fermer Stack Builder.

- Pour ouvrir l'invite de commande "psql", taper psql dans le menu qui s'ouvre lorsque vous appuyez sur la touche *Windows* et ouvrir l'application proposée.

\normalsize

### 0.2 Lancer psql une fois l'installation réussie

\small

- Windows : taper `psql` dans le menu qui s'ouvre lorsque vous appuyez sur la touche *Windows* et ouvrir l'application proposée.

- Linux : saisir `psql -U postgres` dans un terminal puis saisir le mot de passe choisi précédemment.

- MaxOS X : saisir `psql` dans un terminal.

\normalsize

\newpage{}

## 1. Créer une BD spatiale et y charger des données

### 1.1 À propos des données

Les données utilisées dans ce TP proviennent de la [plateforme open-data de l'APUR](https://opendata.apur.org/) (Atelier Parisien d'Urbanisme).

Vous pouvez les récupérer directement à l'URL suivante : [data_seance5.zip](https://mthh.github.io/sig-lp-prog/5/data_seance5.zip)


#### 1.1.1 QUARTIER_DE_PARIS

Source : [https://opendata.apur.org/datasets/quartier-de-paris/explore](https://opendata.apur.org/datasets/quartier-de-paris/explore)

Le jeu de données contient la délimitation des 80 quartiers administratifs de Paris (il s'agit de la division administrative du niveau inférieur à l'arrondissement).

\scriptsize

| Colonne | Description | Type |
|-|-|-|
| N_SQ_QU | Identifiant séquentiel du quartier | Nombre |
| C_QU | Numéro de quartier | Nombre |
| C_QUINSEE | Numéro INSEE du quartier | Nombre |
| L_QU | Nom du quartier | Texte |
| C_AR | Numéro d'arrondissement | Nombre |
| N_SQ_AR | Lien avec l'arrondissement | Nombre |

\normalsize

![&nbsp;](./images/quartier_de_paris_overview.png){ width=60% margin=auto }

\newpage{}

#### 1.1.2 IRIS

Source : [https://opendata.apur.org/datasets/recensement-iris-logement/explore](https://opendata.apur.org/datasets/recensement-iris-logement/explore)

Découpages des 992 IRIS (*Ilots Regroupés pour l'Information Statistique* - voir la [définition sur le site de l'INSEE](https://www.insee.fr/fr/metadonnees/definition/c1523) si besoin) parisiens et données issues du recensement 2015.

\scriptsize

| Colonne | Description          | Type |
|-|-|-|
| n_sq_ir | Identifiant séquentiel de l’IRIS | Nombre |
| c_ainsee | Code de la commune ou de l'arrondissement | Nombre |
| n_qu | Numéro du quartier | Nombre |
| c_ir | Numéro d’IRIS |  Nombre |
| c_typeir | Type de l'IRIS | Texte |
| l_ir | Nom de l’IRIS | Texte |
| nb_log | Nombre de logements | Nombre |
| nb_rp | Nombre de résidences principales | Nombre |
| nb_rseocc | Nombre de résidences secondaires ou à occupation occasionnelle | Nombre |
| nb_logvac | Nombre de logements vacants | Nombre |
| nb_prop | Nombre de ménages propriétaires | Nombre |
| nb_loc_prive | Nombre de ménages en location avec un bailleur privé | Nombre |
| nb_loc_social | Nombre de ménages en location avec un bailleur social | Nombre |
| nb_moy_perspiece | Nombre moyen de personnes par pièce | Nombre |

\normalsize

Puisque `nb_log` désigne le nombre total de logement, `nb_log` = `nb_rp` + `nb_rseocc` + `nb_logvac`

![&#8203;](./images/iris_overview.png){ width=60% margin=auto }

\newpage{}

#### 1.1.3 STATION_DE_TRANSPORT_EN_COMMUN_METRO

Source : [https://opendata.apur.org/datasets/station-de-transport-en-commun/explore](https://opendata.apur.org/datasets/station-de-transport-en-commun/explore)

Localisation des 247 stations de métro situées dans la ville de Paris (les stations de métro hors des limites administratives de Paris n'ont pas été incluses).

\scriptsize

| Colonne | Description | Type |
|-|-|-|
| N_SQ_STC | Identifiant séquentiel de la station | Nombre |
| L_STATION | Nom de la station | Texte |
| C_CORRESP | Type de correspondance ou terminus sur la station | Texte |
| C_NATURE | Type de correspondance ou terminus sur la station | Texte |
| C_NUMLIGNE | Numéro de la ligne | Texte |

\normalsize

Attention l'information `C_NUMLIGNE` ne semble pas complète, en particulier pour les stations utilisées par plusieurs lignes.

![&#8203;](./images/metro_overview.png){ width=60% margin=auto }

\newpage{}


#### 1.1.4 LIGNE_DE_TRANSPORT_EN_COMMUN_METRO

Source : [https://opendata.apur.org/datasets/ligne-de-transport-en-commun/explore](https://opendata.apur.org/datasets/ligne-de-transport-en-commun/explore)

Tracé des lignes du métro parisien, sous forme de 109 tronçons.
Le tracé de certaines lignes dépasse les limites administratives de Paris (les tronçons n'ont pas été redécouper pour exclure les portions hors de Paris).

\scriptsize

| Colonne | Description | Type |
|-|-|-|
| n_qu_lts | Identifiant séquentiel de la station | Nombre |
| l_ligne | Nom de la ligne| Texte |
| n_annee | Année de mise en service du tronçon | Nombre |

\normalsize

![&nbsp;](./images/ligne_metro_overview.png){ width=60% margin=auto }

\newpage{}

### 1.2 Créer une BD et activer l'extension PostGIS

Dans le terminal interactif `psql`, on créé la BD et on active l'extension PostGIS :

```SQL
postgres=# CREATE DATABASE paris;
postgres=# \connect paris
paris=# CREATE EXTENSION postgis;
```


### 1.3 Charger des données spatiales dans la BD

Sur windows, taper `shp2pgsql` dans le menu qui s'ouvre lorsque vous appuyez sur la touche *Windows* et ouvrir l'application *PostGIS Shapefile GUI Loader and Exporter* qui est proposée. L'import se fera à l'aide d'un GUI.

Sur Linux et MacOS X l'import se fait à l'aide d'un utilitaire en ligne de commande nommé `shp2pgsql`.

Lors de l'import, il faut toujours bien spécifier le SCR de la couche importée (en utilisant son code EPSG) ainsi que son encodage. Il faut également avoir connaissance du nom de la BD dans laquelle importer ces fichiers.

Vous aller charger dans votre BD `paris` les 4 couches présentées précédemment.
Pour plus de simplicité, utilisez les noms de table de suivants :

- Couche `QUARTIER_DE_PARIS.shp` → `quartier`
- Couche `RECENSEMENT_IRIS_LOGEMENT.shp` → `iris`
- Couche `STATION_DE_TRANSPORT_EN_COMMUN_METRO.shp` → `station_metro`
- Couche `LIGNE_DE_TRANSPORT_EN_COMMUN_METRO.shp` → `ligne_metro`

Sur Linux et MacOS X la syntaxe à utiliser est la suivante :

```bash
shp2pgsql -s <srid> -c -D -I <chemin du shp a importer> <table à créer> | psql -U <user> -d <BD>
```

Par exemple pour importer la couche `QUARTIER_DE_PARIS.shp` dans la BD `paris`, depuis le dossier `seance5` :

```bash
shp2pgsql -s 2154 -c -D -I QUARTIER_DE_PARIS/QUARTIER_DE_PARIS.shp quartier | psql -U postgres -d paris
```

\newpage{}

## 2. Premières requêtes spatiales

**Vous noterez vos requêtes ainsi que les réponses obtenues dans un document à part.**


### 2.1 Requête spatiale simple (1)

Quel est le nom du plus petit des quartiers parisien ?


### 2.2 Requête spatiale simple (2)

Quelle est la superficie moyenne d'un quartier parisien ?


### 2.3 Requête spatiale simple (3)

Quel est le nom de la station de métro la plus au Nord ?


### 2.4 Requête spatiale simple (4)

Quel est le nom de l'iris qui contient le plus de logements ?

### 2.5 Requête spatiale simple (5)

Quels sont les noms des 5 iris qui contiennent la plus grande part de logements vacants ?


### 2.6 Requête spatiale mobilisant plusieurs tables (1)

Quels quartiers de Paris peuvent désormais bénéficier de la ligne '14' depuis 2020 ?

### 2.7 Requête spatiale mobilisant plusieurs tables (2)

Par quel quartier(s) passe(nt) les tronçons de métro mis en service le plus tôt (c'est à dire en 1900) ?


### 2.8 Requête spatiale mobilisant plusieurs tables (3)

Quel est le nom du quartier qui contient le plus de logements ?


### 2.9 Requête spatiale mobilisant plusieurs tables (4)

Quels sont les noms des 3 quartiers qui contiennent la plus grande part de logements vacants ?

### 2.10 Requête spatiale mobilisant plusieurs tables (5)

Calculer la longueur totale de ligne de métro par quartier.

### 2.11  Requête spatiale mobilisant plusieurs tables (6)

Quelles sont les stations de métro située sur la ligne 14 du métro ?
(attention à ne pas utiliser le champ `c_numligne` de la couche 'station_metro' mais à bien utiliser une relation spatiale)

## 3. Pour aller plus loin

### 3.1 Création d'une table utilisant le résultat d'une requête

Créez une table nommée `arrondissement` décrivant les différents arrondissements parisiens (vous utiliserez pour cela la table `quartier` ainsi que le champ `c_ar`). Cette table doit contenir au moins deux colonnes : numéro de l'arrondissement et géométrie de l'arrondissement.

Vérifiez ensuite, dans la table `geometry_columns` que votre nouvelle table (et sa colonne de géométrie) y apparaît bien :

```sql
paris=# SELECT * FROM geometry_columns;
```

\scriptsize

| f_table_catalog | f_table_schema |  f_table_name  | f_geometry_column | coord_dimension | srid |      type     |  
|-----------------|----------------|----------------|-------------------|-----------------|------|-----------------|
|paris           | public         | quartier       | geom              |               2 | 2154 | MULTIPOLYGON |
|paris           | public         | iris           | geom              |               2 | 2154 | MULTIPOLYGON |
|paris           | public         | station_metro  | geom              |               2 | 2154 | POINT |
|paris           | public         | ligne_metro    | geom              |               2 | 2154 | MULTILINESTRING |
|**paris**           | **public**         | **arrondissement** | **geom**              |               **2** | **2154** | **POLYGON**|

\normalsize

Si la nouvelle table n'y apparaît pas du tout ou que le type de géométrie (`Polygon`) n'est pas détecté correctement, c'est probablement que vous avez fait une erreur.

Si la table y apparaît mais que la valeur du SRID n'est pas correcte (`0` au lieu de `2154` par exemple), regarder sur le Web comment réparer cette informations (*hint* : il existe des fonctions PostGIS dédiées à s'assurer que ces informations sont correctement enregistrées dans la table `geometry_columns` et dédiées à modifier le SRID d'une table existante dans la table `geometry_columns`).

### 3.2 Statistiques spatiales

Comptez le nombre de station de métro par arrondissement.
Quel est l'arrondissement avec le moins de station ? Avec le plus de station ?

Regardons désormais cette information de manière conjointe à la superficie des arrondissements. Quel est l'arrondissement avec le plus de stations par kilomètre carré ? Avec le moins de stations par kilomètre carré ?

### 3.3 Requête spatiale avancée (1)

Quel est le nom de la station de métro la plus éloignée de toute les autres ?


### 3.4 Requête spatiale avancée (2)

Quels sont les noms des deux stations de métro les plus proches l'une de l'autre ?


## 4. Pour aller plus loin...

À l'exception de la question *3.1*, nous n'avons pas créer de table ou de vue.

Admettons que nous voulions produire une carte de la part de logements vacants par quartier de Paris.

- **Quel type de représentation faudrait-il mettre en oeuvre ?** *(repensez au lien entre données statistiques et variables visuelles vu dans le cours de la séance 4)*

- **Quelles étapes devraient être mise en oeuvre ?** *(dans PostGIS, dans QGIS ou l'outil de cartographie choisi, etc.)*

- **Essayez de réaliser cette carte.**