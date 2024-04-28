# Nouveaux imports
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

# Ajout jvideo
from pydantic import BaseModel
from typing import Literal, Optional
from uuid import uuid4
from fastapi.encoders import jsonable_encoder

import json
import os

from fastapi import FastAPI

# Initialisation de l'application
app = FastAPI()

# A placer sous app = FastAPI(). Cette ligne active le moteur de template Jinja et indique que les templates HTML seront stockés dans le dossier "templates"
templates = Jinja2Templates(directory="templates")

# Cette ligne indique que les fichiers statiques (images, css) seront placés dans le dossier nommé "static"
app.mount("/static", StaticFiles(directory="static"), name="static")

# Chargement de la base de données JSON
JV_DATABASE_FILE = "JEUXVIDEOS1.json"

if os.path.exists(JV_DATABASE_FILE):
    with open(JV_DATABASE_FILE, "r") as f:
        JV_DATABASE = json.load(f)

    JV_DATABASE_sorted = sorted(JV_DATABASE, key=lambda x: x['nom'].lower())

# Modification de la route pour renvoyer du HTML
@app.get("/")
async def root(request: Request):
    #return {"message": "Hello World"}
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/jvideos", response_class=HTMLResponse)
async def jvideos(request: Request):
    JV_DATABASE_sorted = sorted(JV_DATABASE, key=lambda x: x['nom'].lower())
    return templates.TemplateResponse("jvideos.html", {"jvideos": JV_DATABASE_sorted, "request" : request})

# Définition d'un objet Jvideo
class Jvideo(BaseModel):
    id_steam: int
    nom: str
    date_sortie: str
    genre: str
    lien_image: str
    emotions: str

@app.get("/ajout-jvideo")
async def ajout_recette(request: Request):
    return templates.TemplateResponse("ajouter_jvideo.html", {"request": request})

# Fonction sans route qui va se charger de traiter les données
# Prend en paramètre en objet Jvideo et l'écrit dans le JSON
def util_ajouter_jvideo(jvideo: Jvideo):
    # Transformer l'objet Jvideo au format JSON
    json_recette = jsonable_encoder(jvideo)
    # Ajouter l'élément au JSON initial (stocké dans la variable globale JV_DATABASE)
    JV_DATABASE.append(json_recette)
    # Écrire ce nouveau JSON dans le fichier externe
    with open(JV_DATABASE_FILE, "w") as f:
        json.dump(JV_DATABASE, f)

@app.post("/ajouter-jvideo", response_class=HTMLResponse)
async def ajouter_jvideo(request: Request):
    # On récupère les valeurs du formulaire
    form_data = await request.form()
    titre = form_data.get('titre') # valeur du champ name="titre" dans le formulaire HTML 
    type_recette = form_data.get('type_recette')

    # On crée un nouvel objet Jvideo pour l'ajouter dans la base
    jvideo = Jvideo(nom=titre, type=type_recette)

    # On fait appel à la fonction extérieure pour gérer l'ajout dans la BDD
    util_ajouter_jvideo(jvideo)

    return templates.TemplateResponse("ajouter_jvideo.html", {"request": request})
