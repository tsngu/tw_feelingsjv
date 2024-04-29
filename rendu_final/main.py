# Nouveaux imports
from fastapi import FastAPI, Request, Form, Query
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
import requests

# Initialisation de l'application
app = FastAPI()

# A placer sous app = FastAPI(). Cette ligne active le moteur de template Jinja et indique que les templates HTML seront stockés dans le dossier "templates"
templates = Jinja2Templates(directory="templates")

# Cette ligne indique que les fichiers statiques (images, css) seront placés dans le dossier nommé "static"
app.mount("/static", StaticFiles(directory="static"), name="static")

# Chargement de la base de données JSON
JV_DATABASE_FILE = "JEUXVIDEOS.json"

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
    emotions_en: str
    emotions_fr: str

@app.get("/recherches", response_class=HTMLResponse)
async def jvideos(request: Request, search: str = Query(None)):
    # Filtrer la base de données si une recherche est effectuée
    if search:
        filtered_jvideos = [jvideo for jvideo in JV_DATABASE if search.lower() in jvideo['nom'].lower() or search.lower() in jvideo['genre'].lower() or search.lower() in jvideo['emotions_en'].lower() or search.lower() in jvideo['emotions_fr'].lower()]
    else:
        filtered_jvideos = JV_DATABASE_sorted
    return templates.TemplateResponse("jvideos.html", {"jvideos": filtered_jvideos, "request" : request})