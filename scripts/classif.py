from utils import *
import csv
from itertools import islice

#id_jeu = "620"
#print(get_main_emotions(id_jeu))

# parcours du fichier .tsv
# le but est d'ajouter les émotions de GoEmotions
# à la dernière colonne du fichier games_data_bdd.csv

chemin = "../meta/games_data_bdd.csv"

nouveau_csv = []
header = []

# on lit le fichier pour trouver l'id_steam
# et faire tourner GoEmotions
with open(chemin, 'r') as bdd:
    reader = csv.reader(bdd, delimiter='\t')
    # j'enregistre le header du fichier csv
    for ligne in islice(reader, 0, 1):
        header = ligne
    # essayons sur 3 reviews déjà...
    for row in tqdm(reader, desc="Analyse jeu par jeu"):
        # extraire code steam
        code_steam = row[0]
        # on le donne à manger à GoEmotions
        emotions = get_main_emotions(code_steam)
        # on crée le contenu du nouveau .csv
        nouvelle_ligne = [row[0], row[1], row[2], row[3], row[4], emotions]
        nouveau_csv.append(nouvelle_ligne)

# j'ajoute le header aux données csv
nouveau_csv = [header] + nouveau_csv

# une fois la lecture finie, on peut remplir
# le nouveau fichier .csv
with open("../meta/bdd_avec_emotions.csv", 'w') as nouvelle_bdd:
    writer = csv.writer(nouvelle_bdd, delimiter='\t')
    writer.writerows(nouveau_csv)
