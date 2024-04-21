from typing import List, Tuple, Dict

def split_text(filename: str) -> List[str]:
    """
        À partir du nom du fichier, renvoie la liste des commentaires,
        séparés par : '\n#####\n'
    """
    with open(filename, 'r') as f:
        content = f.read()
    return content.split("\n#####\n")