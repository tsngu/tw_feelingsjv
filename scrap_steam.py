import re
import requests
import os  
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np

# Fonction pour extraire les chiffres entre /app/ et /titre_du_jeu/
def extract_id(url):
    pattern = r"/app/(\d+)/"  # Utilisation d'une expression régulière
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    else:
        return None

def extraire_avis(apps_id):
    for app_id in apps_id:    
        # Effectuer la requête avec l'ID d'application
        response = requests.get(f'https://store.steampowered.com/appreviews/{app_id}?json=1').json()

        # Vérifier si la requête a réussi
        if response.get('success') == 1:
            # Récupérer les avis
            reviews = response['reviews']
            
            # Écrire les avis dans un fichier
            with open(f"./reviews/{app_id}.txt", "w", encoding="utf-8") as f:
                for review in reviews:
                    f.write(review['review'] + "\n")
        else:
            print(f"La requête pour l'app ID {app_id} a échoué.")

# Read the URLs from file
with open("urls_steam.txt", "r") as file:
    urls = file.readlines()

    # Extract app IDs from URLs
    apps_id = [extract_id(url) for url in urls if extract_id(url)]

# Extract reviews for the games
extraire_avis(apps_id)