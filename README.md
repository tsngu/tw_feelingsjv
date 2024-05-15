# tw_feelingsjv

### Projet en Technique Web (M2 TAL INALCO).
**Analyse de sentiments sur des reviews de jeux vidéos**

Ce projet final a été réalisé pour le cours de Techniques Web du Master TAL à l'INALCO.

Il s'agit d'un recueil d'avis STEAM d'une centaine de jeux vidéos. Deux modules (GoEmotion pour les avis anglophones et Sentiment Analysis French pour les avis francophones) ont analysés les avis pour en faire ressortir, en anglais, les 3 sentiments les plus ressentis et, en français, si les avis sont plutôt côté positif ou négatif.

---

Pour lancer le site, clonez le répertoire de ce git :
```bash
git clone https://github.com/tsngu/tw_feelingsjv.git
```

Accédez au git :
```bash
cd tw_feelingsjv
```

N'oubliez pas d'installer les requirements (juste fastapi et uvicorn) :
```bash
pip install -r requirements.txt
```

Accédez au dossier rendu_final :
```bash
cd rendu_final
```

Lancez l'appli avec (Ne pas oublier de CTRL + ALT + R pour vider son cache si le site ne s'affiche pas correctement ):
```bash
uvicorn main:app --reload
```
