import os
import re

def normalize_text(text):
    # Mettre en minuscule
    text = text.lower()
    # Supprimer tout ce qui n'est pas une lettre, un chiffre ou le caractère '#'
    text = re.sub(r"[^\w\s#]", "", text)
    return text

def normalize_files_in_directory(directory):
    # Parcourir les fichiers dans le répertoire donné
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            input_filepath = os.path.join(directory, filename)
            with open(input_filepath, 'r', encoding='utf-8') as file:
                text = file.read()
            normalized_text = normalize_text(text)
            # Écraser le fichier d'entrée avec le texte normalisé
            with open(input_filepath, 'w', encoding='utf-8') as file:
                file.write(normalized_text)

# Remplacer 'chemin_du_repertoire' par le chemin du répertoire contenant les fichiers .txt à normaliser
directory_path = 'reviews/'
normalize_files_in_directory(directory_path)
