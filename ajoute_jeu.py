#! /usr/bin/env python3

# permet d'ajouter un jeu à partir de la saisie utilisateur

import sqlite3 as sql
import os
import re
import requests

# vérifier que le fichier existe
if not os.path.exists("./JEUXVIDEOS.db"):
    print("ERREUR : la base de données n'existe pas")
    exit(1)

# récupérer la saisie utilisateur
print("Ajout d'un jeu à la base de données : ")
id = input("Lien steam du jeu : ")

# vérification des inputs
if re.match(r"\d{6}", id):
    # on a déjà l'ID
    pass
elif re.match(r"^https://store.steampowered.com", id):
    # on regarde si l'adresse répond bien (code 200)
    response = requests.get(id)
    assert(re.match(r"^2\d\d$", str(response.status_code)))
    # on a un lien, on extrait l'id 
    items = id.split("/")
    for item in items:
        if re.match(r"\d{6}", item):
            id = item
else:
    print("Format d'URL invalide")
    exit(1)

nom = input("Entrer le nom du jeu : ")
date = input("Date de sortie : ")
genre = input("Genre du jeu : ")

# si tout va bien, on enregistre le jeu dans la BDD

BDD = sql.connect("JEUXVIDEOS.db")
curseur = BDD.cursor()

curseur.execute(f"INSERT INTO Jeux (id_steam, nom, date_sortie, genre) VALUES (?, ?, ?, ?)", (id, nom, date, genre))

BDD.commit()
BDD.close()