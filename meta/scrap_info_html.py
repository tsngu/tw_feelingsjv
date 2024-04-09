import requests
import sys 
from bs4 import BeautifulSoup
import csv 

def get_app_id(url):
    '''
    Fonction qui prend en argument un url et qui en extrait l'id du jeu.  
    '''
    # Supprimer le texte inutile à la fin de l'URL
    url = url.strip().split('?')[0]
    
    # Extraire l'ID du jeu de l'URL
    url_parts = url.split('/')
    if len(url_parts) >= 3:
        app_id = url_parts[-3] if url.endswith('/') else url_parts[-2]
        print("App ID:", app_id)
        return app_id
    else:
        print("L'URL ne semble pas être au bon format.")
        return None


def get_game_data(url):

    app_id = get_app_id(url)
    api_url = f'https://store.steampowered.com/api/appdetails?appids={app_id}'
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        game_data = data[app_id]['data']
        genre = ", ".join([genre["description"] for genre in game_data.get("genres", [])])
        release_date = game_data.get("release_date", {}).get("date", "")
        #print (release_date)
        game_data["genre"] = genre
        game_data['ID'] = app_id
        #print(genre)
        game_data["date_sortie"] = release_date
        return game_data
    else:
        print(f"La requête HTTP a échoué pour l'URL {url} avec le code:", response.status_code)
        return None

def save_to_csv(game_data_list, filename):
    # Les catégories nécessaires : nom, genre, id steam, date de sortie
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['ID','Titre', 'release_date', 'Genre','Lien_image']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames,delimiter='\t')
        writer.writeheader()
        for game_data in game_data_list:
            writer.writerow({'ID' : game_data.get('ID',''),
                             'Titre': game_data.get('name', ''),
                             'release_date' : game_data.get('date_sortie',''), 
                             'Genre': game_data.get('genre', ''), 
                             'Lien_image': game_data.get('header_image', ''),
                             })

def main(input_file, output_file):
    game_data_list = []
    with open(input_file, 'r') as f:
        for url in f:
            url = url.strip() 
            game_data = get_game_data(url)
            if game_data:
                game_data_list.append(game_data)
    save_to_csv(game_data_list, output_file)
    print("Données sauvegardées dans", output_file)

if __name__ == "__main__":
    input_file = 'urls_steam.txt'
    output_file = 'games_data.csv'  # Le fichier CSV où vous voulez sauvegarder les données
    main(input_file, output_file)
