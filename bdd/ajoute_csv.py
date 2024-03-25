#!/usr/bin/env python3

# à partir d'un csv fourni par Fanny
# remplit la base de données

import csv
import sqlite3 as sql
import os
import re
import requests

# vérifier que le fichier existe
if not os.path.exists("./JEUXVIDEOS.db"):
    print("ERREUR : la base de données n'existe pas")
    exit(1)

# ouvre la BDD
BDD = sql.connect("JEUXVIDEOS.db")
curseur = BDD.cursor()

PATH = "../data/"
with open(PATH+"jeuxvideos.csv", "rt") as fichierJV:
    CSV_JV = csv.DictReader(fichierJV, delimiter="\t")
    for ligne in CSV_JV:
        curseur.execute("INSERT INTO Jeux (id_steam, nom, date_sortie, genre, lien_image) VALUES (:idsteam, :nom, :date_sortie, :genre, :lien_image)", ligne)

BDD.commit()
BDD.close()
