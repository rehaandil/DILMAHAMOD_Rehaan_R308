# TP1 - Partie D 
import random


# Lit les mots du fichier (même fonction que la partie C)
def charger_mots(nom_fichier):
    mots = []
    try:
        fichier = open(nom_fichier, "r", encoding="utf-8")
        for ligne in fichier:
            ligne = ligne.strip()
            if ligne != "":
                mots.append(ligne)
        fichier.close()
    except FileNotFoundError:
        mots = ["python", "reseau", "routeur"]
    return mots


# Remplace les lettres accentuées : ÉLÉPHANT -> ELEPHANT (défi du prof)
def enlever_accents(mot):
    accents = {"É": "E", "È": "E", "Ê": "E", "Ë": "E", "À": "A", "Â": "A",
               "Î": "I", "Ï": "I", "Ô": "O", "Ù": "U", "Û": "U", "Ç": "C"}
    nouveau = ""
    for lettre in mot:
        if lettre in accents:
            nouveau = nouveau + accents[lettre]  # lettre accentuée -> sans accent
        else:
            nouveau = nouveau + lettre  # lettre normale -> on la garde
    return nouveau


# Lit scores.txt (nom:victoires). S'il n'existe pas, on part de zéro
def charger_scores():
    scores = {}
    try:
        fichier = open("scores.txt", "r", encoding="utf-8")
        for ligne in fichier:
            morceaux = ligne.strip().split(":")
            if len(morceaux) == 2:
                try:
                    scores[morceaux[0]] = float(morceaux[1])
                except ValueError:
                    print("Ligne ignorée :", ligne)
        fichier.close()
    except FileNotFoundError:
        print("Pas encore de scores, on part de zéro")
    return scores


# Réécrit scores.txt à la fin du programme
def sauvegarder_scores(scores):
    try:
        fichier = open("scores.txt", "w", encoding="utf-8")
        for nom in scores:
            fichier.write(nom + ":" + str(scores[nom]) + "\n")
        fichier.close()
    except OSError:
        print("Impossible d'écrire scores.txt")


# Joue une partie de pendu. Renvoie True si gagné, False si perdu
def jouer(mot):
    masque = ["_"] * len(mot)  # le mot caché
    erreurs = 0
    deja_proposees = []  # lettres déjà tapées

    # on joue tant qu'on n'a pas 7 erreurs et qu'il reste des "_"
    while erreurs < 7 and "_" in masque:
        print()
        print("Mot :", " ".join(masque))  # affiche "P _ T _ _ N"
        print("Erreurs :", erreurs, "/ 7")
        print("Lettres proposées :", deja_proposees)
        lettre = input("Lettre : ").upper()
        lettre = enlever_accents(lettre)  # "é" tapé devient "E"

        if len(lettre) != 1 or not lettre.isalpha():
            print("Tape une seule lettre !")
        elif lettre in deja_proposees:
            print("Déjà proposée, pas d'erreur en plus")
        else:
            deja_proposees.append(lettre)
            if lettre in mot:
                # on révèle la lettre à toutes ses positions dans le masque
                for i in range(len(mot)):
                    if mot[i] == lettre:
                        masque[i] = lettre
            else:
                erreurs = erreurs + 1
                print("Raté !")

    # fin de partie : plus de "_" = gagné, sinon perdu
    if "_" not in masque:
        print("Gagné ! Le mot était", mot)
        return True
    else:
        print("Perdu, le mot était", mot)
        return False


# ---- Programme principal
scores = charger_scores()
mots = charger_mots("mots.txt")
nom = input("Ton nom : ")
mode = input("1 ou 2 joueurs ? ")

rejouer = "o"
while rejouer == "o":
    if mode == "2":
        # mode 2 joueurs : le joueur 1 choisit le mot
        mot = input("Joueur 1, tape le mot secret : ")
        print("\n" * 50)  # 50 lignes vides pour cacher le mot
    else:
        mot = random.choice(mots)  # mode 1 joueur : mot au hasard
    mot = enlever_accents(mot.upper())  # "Python" -> "PYTHON", "Éléphant" -> "ELEPHANT"

    if jouer(mot):
        # victoire : +1 au score du joueur (0 s'il est nouveau)
        scores[nom] = scores.get(nom, 0.0) + 1

    rejouer = input("Rejouer ? (o/n) ")

sauvegarder_scores(scores)
print("Scores :", scores)