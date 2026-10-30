"""
TP2 R3.08 - Jeux d'essai de la partie C et des bonus.
Lancer ce fichier avec F5 dans Thonny : tout est automatique (pas de saisie).
"""

from jeu import Partie, championnat
from joueurs import JoueurIA, JoueurIAMalin

# ---- Jeu d'essai de l'énoncé : IA contre IA, 20 parties ----
# Attendu : chaque partie se termine par une victoire ou un nul, sans plantage.
score = championnat(JoueurIA("IA 1"), JoueurIA("IA 2"), 20)
print("IA vs IA (20 parties)          :", score)

# assert vérifie une condition : si elle est fausse, le programme s'arrête
# avec une erreur. Ici : le total victoires + nuls doit faire 20.
assert sum(score.values()) == 20, "Une partie ne s'est pas terminée correctement"

# ---- Bonus : IA maligne contre IA aléatoire ----
# L'IA maligne devrait gagner bien plus souvent et ne presque jamais perdre.
score = championnat(JoueurIAMalin("Malin"), JoueurIA("Hasard"), 20)
print("IA maligne vs IA (20 parties)  :", score)

# ---- Une partie complète affichée pour voir le déroulement ----
print("\n--- Exemple de partie IA vs IA ---")
Partie(JoueurIA("IA 1"), JoueurIA("IA 2")).jouer()
