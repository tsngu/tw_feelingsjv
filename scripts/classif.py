from tqdm import tqdm
from utils import *

example_sentence = "Hello, my dog is cute"

# exemple du corpus :
avis = split_text("scraping/reviews_en/620.txt")
example = avis[0]

print(get_emotions(example))

#print(len(avis)) # 301

# pour chaque avis, on range les sentiments dans un dictionnaire et on compte les occurrences
sentiments = defaultdict(int)

for review in tqdm(avis, desc="Processing review"):
    emotions = get_emotions(review)
    for each in emotions:
        sentiments[each] += 1

print(sentiments)

# on parcourt les avis 1 à 1 et on remplit

#print(f"Example sentence: \n{example}\n")
#print("\n******************************\n")
#print("Predicted emotions: ")
