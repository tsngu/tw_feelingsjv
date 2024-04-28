import torch
from transformers import AutoTokenizer, RobertaForSequenceClassification
from collections import defaultdict
from typing import List, Dict, Tuple
from tqdm import tqdm

id2label = {0:"admiration",
            1:"amusement",
            2:"anger",
            3:"annoyance",
            4:"approval",
            5:"caring",
            6:"confusion",
            7:"curiosity",
            8:"desire",
            9:"disappointment",
            10:"disapproval",
            11:"disgust",
            12:"embarrassment",
            13:"excitement",
            14:"fear",
            15:"gratitude",
            16:"grief",
            17:"joy",
            18:"love",
            19:"nervousness",
            20:"optimism",
            21:"pride",
            22:"realization",
            23:"relief",
            24:"remorse",
            25:"sadness",
            26:"surprise",
            27:"neutral"}

def split_text(filename: str) -> List[str]:
    """
        À partir du nom du fichier, renvoie la liste des commentaires,
        séparés par : '\n#####\n'
    """
    with open(filename, 'r') as f:
        content = f.read()
    return content.split("\n#####\n")

def get_emotions(example:str) -> List[str]:
    """
        À partir d'une chaîne de caractères donnée en entrée,
        donne la liste des émotions détectées par GoEmotion
    """
    res = []
    tokenizer = AutoTokenizer.from_pretrained("bsingh/roberta_goEmotion")
    model = RobertaForSequenceClassification.from_pretrained("bsingh/roberta_goEmotion", problem_type="multi_label_classification")
    # les paramètres du Tokenizer permettent de prendre en compte les limitations de GoEmotions
    # (max 512 tokens par message). On choisit de tronquer les reviews trop longues.
    inputs = tokenizer(example, max_length=512, truncation=True, return_tensors="pt")
    # calcul de la longueur en tokens de l'input :
    num_elements_input_ids = inputs['input_ids'].numel()
    with torch.no_grad():
        logits = model(**inputs).logits
    predicted_class_ids = torch.arange(0, logits.shape[-1])[torch.sigmoid(logits).squeeze(dim=0) > 0.5]
    for code in predicted_class_ids:
        res.append(id2label[code.item()]) # .item() pour obtenir le int à partir de tensor(3) par ex
    return res

def get_main_emotions(game_id: str) -> List[str]:
    """
        Étant donné l'ID steam d'un jeu, renvoie une chaîne des des 3 émotions
        les plus représentées d'après GoEmotions, séparées par des + (fichier .tsv)
    """
    sentiments = defaultdict(int)
    # extraction du corpus
    avis = split_text(f"../scraping/reviews_en/{game_id}.txt")
    for review in tqdm(avis, desc="Processing review"):
        emotions = get_emotions(review)
        for each in emotions:
            sentiments[each] += 1
    # maintenant on range le dictionnaire par valeur décroissante :
    sorted_items = sorted(sentiments.items(), key=lambda x: x[1], reverse=True)
    # Take the top three items (keys with highest values)
    top_three = sorted_items[:3]
    # [('neutral', 288), ('excitement', 265), ('amusement', 255)]
    return "+".join([top_three[0][0], top_three[1][0], top_three[2][0]])