# COMPTE-RENDU

Comme nous l'avions précédemment expliqué dans notre cahier des charges. Nous souhaitons mettre à disposition un site internet qui permet à l'utilisateur, pour une centaine de jeu, de connaître les 3 émotions principales que l'on peut recueillir à partir des commentaires laissés sur la plateforme steam.

## Étapes du projet

### 1. Sélection des jeux et recueil des liens steam (Tifanny)
La première partie du travail consistait à constituer une liste de jeu ainsi que leur lien steam afin de pouvoir extraire les informations nécessaires à la conception du site.
Ainsi, 100 liens pour 100 jeux ont été rassemblés dans un fichier txt. À cela s'ajoute les reviews en français et en anglais. Ces datas seront par la suite utilisées pour faire de l'analyse de sentiments. Chaque avis est dans un fichier txt que l'on retrouve dans les dossiers "reviews" et "reviews_en".
Ces dossiers se trouvent dans le dossier "scraping" dans lequel on retrouve également les scripts suivants :
- scrap_steam.py : permet de récupérer les reviews en ayant la capacité de modifier les hyperparamètres afin de déterminer ce que l'on veut scrapper.
- norm.py : permet de normaliser les reviews qui ont été récupérées.

### 2. Extraction des méta-informations (Fanny)

Une fois les liens manuellement relevés d'une part et les avis automatiquements récupérés d'une autre part, la seconde partie du travail consiste à récupérer les métadonnées des jeux à partir des urls.
Dans le fichier méta, il y a le script scrap_info_html.py qui permet dans un premier temps d'extraire l'ID du jeu pour ensuite interroger l'API et extraire les données suivantes et de les stocker dans un fichier csv :
- l'ID du jeu
- Son nom
- Sa date de sortie
- Genre(s) du jeu
- Lien vers l'image du jeu
Le fichier généré est "games_data_csv", que l'on peut modifier manuellement (notamment les noms de colonnes) pour plus facilement le rentrer dans solr.

### 2bis. Création d'une base de données (Clément)

En parallèle de la création d'un fichier csv contenant les métadonnées, nous avons pensé qu'il pourrait être utile de créer une base de données pour stocker les données en vue de les exploiter sur le site internet.
Il s'avère que ça n'était pas vraiment nécessaire puisqu'un fichier csv est suffisant avec l'utilisation de solr.
Il est néamoins possible d'accéder aux fichiers de créations de la base de données dans le dossier "bdd".

### 3. Analyse de sentiments en anglais et en français (Clément)

Afin de faire de l'analyse d'émotion en anglais, nous avons utilisé [roberta_goEmotion](https://huggingface.co/bsingh/roberta_goEmotion), qui permet d'annoter selon 28 émotions différentes. Ces annotations en sentiment sont ensuite ajoutées à la base de données dans la colonne "emotions_en".
Nous avons fait les manipulations suivantes pour générer les émotions pour les deux langues.

#### 3.1. Pour l'anglais, avec roberta_goEmotion

Pour l'anglais : il s'agit du modèle Roberta entraîné sur un corpus de commentaires Reddit (58k). Annoté avec 28 émotions différentes (optimisme, neutre, déception etc.). Pour chaque jeu, on extrait les 3 émotions les plus fréquentes dans le corpus de reviews.
Pour retrouver les scripts permettant de générer les émotions en anglais, il faut se rendre dans le dossier `scripts/`.
- utils.py => toutes les fonctions nécessaires
- classif.py => permet de lire et d'écrire dans le tsv les émotions en anglais.

#### 3.2. Pour l'anglais, avec Sentiment_Analysis_French

Nous utilisons un autre modèle : [Sentiment_Analysis_French](https://huggingface.co/ac0hik/Sentiment_Analysis_French/tree/main)
Il s'agit d'un fine-tuning du modèle camembert, sur un corpus de tweets.
Le modèle pour le français n'est pas aussi performant, ainsi les commentaires sont uniquement décrits par : positif, négatif ou neutre. Pour chaque jeu, on renvoie l'annotation la plus fréquente (une seule). On ajoute cette information dans une colonne "emotions_fr".
Pour retrouver les scripts permettant de générer les émotions en français, il faut se rendre dans le dossier `scripts/`.
- utils.py => toutes les fonctions nécessaires
- classif_fr.py => permet de lire et d'écrire dans le tsv les émotions en français.


### 4. Création de l'interface (Tifanny)

Nous avons chercher à créer une interface graphique la plus proche du scénario utilisateur, disponible dans notre cahier des charges.
Nous sommes allés au plus simple en prenant le format galerie, avec un pop-up s'affichant lorsque l'on clique sur le jeu vidéo (s'affiche alors le titre du jeu, la date de sortie, son genre et les émotions les plus représentatives en français et en anglais.)
Nous utilisons une fastAPI pour connecter l'interface du site à notre base de données en format json.
Il est possible de retrouver les codes dans le dossier "site"
Pour lancer le site, il faut depuis le dossier faire la commande suivante :
``` bash
$ uvicorn main:app --reload
```

### 5. Rédaction du présent compte-rendu (Fanny)
