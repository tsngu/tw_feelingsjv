import re
import requests
import os
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

# Fonction pour extraire les chiffres entre /app/ et /titre_du_jeu/
def extract_id(url):
    pattern = r"/app/(\d+)/"  # Utilisation d'une expression régulière
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    else:
        return None

def extraire_n_avis(app_id, n=300):
    reviews = []
    cursor = '*'
    params = {
        'json': 1,
        'filter': 'all',
        'language': 'english',
        'day_range': 9223372036854775807,
        'review_type': 'all',
        'purchase_type': 'all',
        'cursor': cursor,
        'num_per_page': 100
    }

    while n > 0:
        params['cursor'] = cursor.encode()
        params['num_per_page'] = min(100, n)

        response = requests.get(f'https://store.steampowered.com/appreviews/{app_id}', params=params).json()

        # Check if 'cursor' exists in the response
        if 'cursor' not in response:
            break

        cursor = response['cursor']
        reviews += response['reviews']
        n -= 100

        if len(response['reviews']) < 100:
            break

    return reviews

# Lis les URLs du fichiers
with open("urls_steam.txt", "r") as file:
    urls = file.readlines()

    # Extrait les IDs
    apps_id = [extract_id(url) for url in urls if extract_id(url)]

# Extrait les reviews pour chaque jeu
for app_id in apps_id:
    reviews = extraire_n_avis(app_id)
    
    with open(f"./reviews_en/{app_id}.txt", "w", encoding="utf-8") as f:
        for review in reviews:
            f.write(review['review'] + "\n\n#####\n\n")