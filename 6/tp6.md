---
title: "Module SIG - Séance 6 - 2022-2023"
author: [Matthieu Viry]
date: "2023-02-08"
linkcolor: blue
header-includes: |
	\usepackage{caption}
	\captionsetup[figure]{
      name=,
      labelsep=none,
      labelformat=empty}
...

# Séance 6 - TP - PostGIS 2

## 0. Préambule

Dans ce TP nous allons revisiter l'analyse menée par John Snow lors de l'épidémie de cholera survenue à Londres en 1854.

Pour cela nous disposons de deux couches de données téléchargeables [ici](https://mthh.github.io/sig-lp-prog/6/data_seance6.zip) :

- l'emplacement des pompes à eau (SCR : EPSG 27700),
- l'emplacement des lieux de résidence des personnes décédées (SCR : EPSG 27700) - le nombre de décès par lieu de résidence est contenu dans les attributs.

![&nbsp;](./images/seance5.png){ width=50% margin=auto }

Au cours de ce TP nous allons mettre en oeuvre deux méthodes différentes d'analyse spatiale afin de détecter la pompe à eau responsable de la propagation du choléra.

Nous chercherons ensuite à cartographier ces résultats dans QGIS pour produire une carte présentant les résultats.
Nous exporterons également une version de la carte produite vers une page Web.

Conseils:

- Notez vos requêtes SQL dans un document à part.
- Sauvegardez vos résultats dans une vue ou une table (temporaire ou non) lorsque vous en êtes satisfaits.
- N'hésitez pas à explorer la [documentation PostGIS](https://postgis.net/docs/reference.html), à chercher sur le Web ou à poser des questions.

## 1. Création d'un BD spatiale et import des données

Sur la base des connaissances acquises dans le TP précédent :

1. Créer une nouvelle base de données nommée "cholera".

2. Activer l'extension PostGIS pour cette BD.

3. Importer la couche "Pumps.shp" et la couche "Cholera_Death.shp" dans la BD "cholera".

## 2. Se connecter à la BD depuis QGIS

Pour une meilleure expérience utilisateur, nous utiliserons QGIS et son extension *DB Manager* dans ce TP.

Pour cela, il faut tout d'abord créer une connection à la BD à utiliser :
- soit en allant dans l'explorateur puis en faisant un clic-droit sur PostGIS, puis en cliquant sur *Nouvelle connection...*
- soit en allant dans le menu *Couche > Ajouter une couche > Ajouter des couches PostGIS...*

![&nbsp;](./images/connection-postgis1.png){ width=60% margin=auto }

Il faut ensuite saisir les informations de connection (hôte, port, etc.) ainsi que les options d'identification éventuelles (*username*, *password*)

![&nbsp;](./images/connection-postgis2.png){ width=80% margin=auto }

Une fois la connection à la BD effectuée, il faut utiliser l'extension *DB Manager* (celle-ci est installée par défaut dans QGIS mais il faut parfois l'activer manuellement en allant dans le menu *Extensions > Installer/Gérer les extensions* puis en s'assurant qu'elle est bien activée / cochée).

L'extension *DB Manager* est accessible depuis le menu *Base de données > Gestionnaire BD...*.
Vous y sélectionnerez votre BD "cholera".
Vous pourrez ensuite voir un aperçu de ses tables et des données qu'elles contiennent. Vous pourrez également ouvrir un onglet vous permettant de saisir vos requêtes SQL (il sera ensuite possible de simplement créer une vue ou une nouvelle table avec le résultat, ainsi que d'afficher les résultats obtenus sur la carte si ils contiennent une géométrie).

![&nbsp;](./images/qgis-gestionnaire-bd.png){ width=100% margin=auto }

\newpage{}

## 2. 1ère méthode : polygones de Voronoï

Un diagramme de Voronoï est un découpage d'un plan en cellules (régions adjacentes, matérialisées par des polygones) à partir d'un ensemble discret de points. Chaque cellule enferme un seul point, et inclut l'ensemble de l'espace du plan qui est le plus proche de ce point que d'aucun autre. La cellule représente en quelque sorte la "zone d'influence" du point qu'elle renferme.

![&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Source : Wikimedia - License : CC BY-SA 3.0](./images/Coloured_Voronoi_2D.png){ width=40% }

Consigne :

- **Vous devez créer les polygones de Voronoï correspondant à la localisation des pompes, puis compter le nombre de décès dans chacune des cellules, puis joindre cette informations à la couche des pompes**.

- **Vous stockerez les résultats (une couche avec les polygones de Voronoï et une avec le nombre de décès joint à la localisation des pompes) chacun dans une _vue_ ou dans une _table_**.


## 2. 2ème méthode : calcul du plus proche voisin et création de lignes

Une autre méthode pouvant être mise en oeuvre est de chercher, pour chaque lieu de décès, la pompe la plus proche.

Consigne :

- **Vous devez chercher, pour chaque lieu de décès, la pompe la plus proche, et créer une ligne droite reliant le reliant à la pompe la plus proche.**

- **Vous stockerez les résultats (une couche de ligne) dans une _vue_ ou dans une _table_**.


## 3. Visualisation dans QGIS

Nous allons désormais revenir dans le logiciel QGIS. Celui-ci permet de facilement se connecter à une base de données.

Comme nous l'avons vu hier, la représentation la plus appropriée pour représenter une variable quantitative absolue (ici *le nombre de décès par pompe*) est l'utilisation de symboles proportionnels.

Consigne :

- **Se connecter à la BD "choléra".**

- **Afficher les couches "choleta_deaths" et "pumps".**

- **Afficher les couches issues des questions 2 et 3 : les polygones de Voronoï, la localisation des pompes avec le nombre de décès, les lignes reliant pompes et décès.**

- **Utiliser les options de symbologies de QGIS pour produire une carte similaire à celle présentée en page 1 de ce TP :**
  * Faire figurer les points représentants les décès (éventuellement afin que leurs tailles soient proportionnels au nombre de décès).
  * Faire figurer les points représentants les pompes afin que leurs tailles soient proportionnels au nombre de décès.
  * Faire figurer le tracé (utiliser un fond transparent) les polygones de Voronoï que vous avez créé.
  * Faire figurer les lignes entre les lieux de décès et les pompes que vous avez créé.


## 4. Export de la carte vers une page Web

Il existe un plugin QGIS nommé *qgis2web* permettant d'exporter les couches présentes dans un projet QGIS vers une page Web utilisant une des bibliothèques de Web-Mapping bien connue (OpenLayers, Leaflet et Mapbox GL JS sont proposées).

**Installez ce plugin** (Menu *Extensions > Installer/Gérer les extensions*)

**Créez une carte Web avec ce plugin**. Que constatez-vous ?

En fonction de la manière dont vous avez créé vos points proportionnels, ceux-ci peuvent désormais tous apparaître de la même taille dans la carte Web. Si c'est le cas, **essayez de configurer vos symboles proportionnels autrement dans QGIS afin que leur taille soit respectée dans la carte Web exportée avec _qgis2web_**.
