#! /usr/bin/env python3

import sqlite3 as sql
import os

if not os.path.exists("./JEUXVIDEOS.db"):
    print("ERREUR : la base de données n'existe pas")
    exit(1)

BDD = sql.connect("JEUXVIDEOS.db")
curseur = BDD.cursor()

curseur.execute("SELECT DISTINCT id_steam, nom, date_sortie, genre FROM Jeux")
res = curseur.fetchall()

for (id, nom, date, genre) in res:
    print(f"{nom} ({genre}) : id steam {id}, sorti le {date}")

BDD.commit()
BDD.close()