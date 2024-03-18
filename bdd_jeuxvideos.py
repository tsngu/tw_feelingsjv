#! /usr/bin/env python3

# base de données de jeux vidéos
#
# contient les informations suivantes :
# titre
# photo
# année de sortie
# genre
# lien vers le site steam

import sqlite3 as sql
import csv

BDD = sql.connect("JEUXVIDEOS.db")
curseur = BDD.cursor()

# création d'une table JEUX
curseur.execute("CREATE TABLE Jeux (id_steam TEXT PRIMARY KEY, nom TEXT NOT NULL, date_sortie TEXT NOT NULL, genre TEXT NOT NULL, lien_steam TEXT NOT NULL);")

# on ajoute une instance 
curseur.execute("INSERT INTO Jeux (id_steam, nom, date_sortie, genre, lien_steam) VALUES (\"413150\", \"Stardew Valley\", \"26 février 2016\", \"farming\", \"https://store.steampowered.com/app/413150/Stardew_Valley/\")")

# on affiche toute la base de données
curseur.execute("SELECT nom, date_sortie, genre FROM Jeux")
result = curseur.fetchall()
print(result)

BDD.commit()
BDD.close()