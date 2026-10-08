# TP1 - Partie C 
import random


# Lit le fichier et renvoie la liste des mots
def charger_mots(nom_fichier):
    mots = []
    try:
        fichier = open(nom_fichier, "r", encoding="utf-8")
        for ligne in fichier:
            ligne = ligne.strip()  # enlève le retour à la ligne
            if ligne != "":  # on ignore les lignes vides
                mots.append(ligne)
        fichier.close()
    except FileNotFoundError:
        # pas de fichier : on utilise une petite liste par défaut
        print("Fichier absent, liste par défaut")
        mots = ["python", "reseau", "routeur"]
    return mots


# Choisit un mot au hasard et le met en MAJUSCULES
def choisir_mot(liste):
    return random.choice(liste).upper()


# Crée le masque : un "_" par lettre du mot
def masque(mot):
    return ["_"] * len(mot)  # ex : 6 lettres -> ['_', '_', '_', '_', '_', '_']


# Tests
liste = charger_mots("mots.txt")
print("Mots :", liste)
print("Mot choisi :", choisir_mot(liste))
print(masque("PYTHON"))