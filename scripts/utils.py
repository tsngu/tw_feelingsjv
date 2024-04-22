import torch
from transformers import AutoTokenizer, RobertaForSequenceClassification
from collections import defaultdict
from typing import List, Dict, Tuple

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
    res = []
    tokenizer = AutoTokenizer.from_pretrained("bsingh/roberta_goEmotion")
    model = RobertaForSequenceClassification.from_pretrained("bsingh/roberta_goEmotion", problem_type="multi_label_classification")
    inputs = tokenizer(example, return_tensors="pt")
    # calcul de la longueur en tokens de l'input :
    num_elements_input_ids = inputs['input_ids'].numel()
    # GoEmotions n'accepte que les inputs de moins de 512 tokens
    if num_elements_input_ids > 512:
        # on a un problème
        # soit on tronque, soit on transforme en 2 reviews
        # ok on fait 2 review. et ensuite on fusionne les listes d'émotions pour que ça ne compte qu'une fois
        return []

    #print("********* INPUTS **********")
    #print("Nombre de tokens : ", num_elements_input_ids)
    #print(inputs)
    # éléments du premier tenseur

    with torch.no_grad():
        logits = model(**inputs).logits
    predicted_class_ids = torch.arange(0, logits.shape[-1])[torch.sigmoid(logits).squeeze(dim=0) > 0.5]
    for code in predicted_class_ids:
        res.append(id2label[code.item()]) # .item() pour obtenir le int à partir de tensor(3) par ex
    return res