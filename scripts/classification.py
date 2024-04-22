from utils import *
import torch
from transformers import AutoTokenizer, RobertaForSequenceClassification

# chargement du modèle GoEmotion
tokenizer = AutoTokenizer.from_pretrained("bsingh/roberta_goEmotion")
model = RobertaForSequenceClassification.from_pretrained("bsingh/roberta_goEmotion")

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

with torch.no_grad():
    logits = model(**inputs).logits

# essai sur un exemple du corpus
avis = split_text("scraping/reviews_en/620.txt")
example = avis[0]

# tokenisation de l'input
tokenised_example = tokenizer(example, return_tensors="pt")

num_labels = len(model.config.id2label)

model = RobertaForSequenceClassification.from_pretrained("bsingh/roberta_goEmotion", num_labels=num_labels)

# prédiction du modèle
outputs = model.predict(tokenised_example)

print(outputs)