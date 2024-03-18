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
curseur.execute("CREATE TABLE Jeux (nom TEXT PRIMARY KEY, date_sortie TEXT NOT NULL, genre TEXT NOT NULL, lien_steam TEXT NOT NULL);")