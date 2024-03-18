#! /usr/bin/env python3

# permet d'ajouter un jeu à partir de la saisie utilisateur

import sqlite3 as sql
import os
import re

# vérifier que le fichier existe
if not os.path.exists("./JEUXVIDEOS.db"):
    print("ERREUR : la base de données n'existe pas")
    exit(1)

# récupérer la saisie utilisateur
print("Ajout d'un jeu à la base de données : ")
id = input("ID steam du jeu : ")
nom = input("Entrer le nom du jeu : ")
date = input("Date de sortie : ")
genre = input("Genre du jeu : ")

# vérification des inputs
assert(re.match(r"\d", id)) # id à 6 chiffres

# si tout va bien, on enregistre le jeu dans la BDD

BDD = sql.connect("JEUXVIDEOS.db")
curseur = BDD.cursor()

curseur.execute(f"INSERT INTO Jeux (id_steam, nom, date_sortie, genre) VALUES (?, ?, ?, ?)", (id, nom, date, genre))

BDD.commit()
BDD.close()