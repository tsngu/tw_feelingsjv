import torch
from utils import *
from transformers import AutoTokenizer, RobertaForSequenceClassification

tokenizer = AutoTokenizer.from_pretrained("bsingh/roberta_goEmotion")
model = RobertaForSequenceClassification.from_pretrained("bsingh/roberta_goEmotion", problem_type="multi_label_classification")

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

example_sentence = "Hello, my dog is cute"

# exemple du corpus :
avis = split_text("scraping/reviews_en/620.txt")
example = avis[0]

inputs = tokenizer(example, return_tensors="pt")

with torch.no_grad():
    logits = model(**inputs).logits

predicted_class_ids = torch.arange(0, logits.shape[-1])[torch.sigmoid(logits).squeeze(dim=0) > 0.5]

print(f"Example sentence: \n{example}\n")
print("\n******************************\n")
print("Predicted emotions: ")

for code in predicted_class_ids:
    print(id2label[code.item()]) # pour obtenir le int à partir de tensor(3) par ex.
    #print((model.config.id2label[code]))




# To train a model on `num_labels` classes, you can pass `num_labels=num_labels` to `.from_pretrained(...)`
num_labels = len(model.config.id2label)
model = RobertaForSequenceClassification.from_pretrained(
    "bsingh/roberta_goEmotion", num_labels=num_labels, problem_type="multi_label_classification"
)

labels = torch.sum(
    torch.nn.functional.one_hot(predicted_class_ids[None, :].clone(), num_classes=num_labels), dim=1
).to(torch.float)
loss = model(**inputs, labels=labels).loss