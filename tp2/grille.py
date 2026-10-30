"""
TP2 R3.08 - Partie A : classe Grille du morpion.

Ce fichier définit la classe Grille, qui représente le plateau de jeu 3x3.
Elle sait :
  - s'afficher à l'écran,
  - recevoir un coup (en vérifiant qu'il est valide),
  - dire si un joueur a gagné,
  - dire si elle est pleine (match nul possible).

Convention de coordonnées (déduite du jeu d'essai de l'énoncé) :
  x = numéro de LIGNE   (0 = en haut, 2 = en bas)
  y = numéro de COLONNE (0 = à gauche, 2 = à droite)
On accède donc à une case avec self.cases[x][y].
"""


class Grille:
    """Grille de morpion 3x3, stockée sous forme de liste de listes."""

    # Attribut de CLASSE (partagé par toutes les grilles) :
    # le caractère qui représente une case vide.
    # On l'utilise partout au lieu d'écrire " " en dur, comme ça
    # si on veut changer de symbole, on ne le change qu'ici.
    VIDE = " "

    def __init__(self):
        """Constructeur : appelé automatiquement quand on écrit Grille()."""
        # On crée 3 lignes, chacune contenant 3 cases vides.
        # IMPORTANT : on utilise une compréhension de liste pour créer
        # 3 listes DIFFÉRENTES en mémoire.
        # Si on écrivait [[" "] * 3] * 3, les 3 lignes seraient la MÊME
        # liste : modifier une case modifierait toute la colonne !
        self.cases = [[Grille.VIDE] * 3 for _ in range(3)]
        # Résultat : [[" ", " ", " "],
        #             [" ", " ", " "],
        #             [" ", " ", " "]]

    def afficher(self):
        """Affiche la grille de façon lisible dans la console."""
        # enumerate() donne à la fois l'indice i (0, 1, 2) et la ligne.
        for i, ligne in enumerate(self.cases):
            # " | ".join(["X", "O", " "]) donne "X | O |  "
            # On ajoute un espace devant et derrière pour centrer.
            print(" " + " | ".join(ligne) + " ")
            # On trace un séparateur ENTRE les lignes,
            # donc pas après la dernière (i == 2).
            if i < 2:
                print("-----------")

    def est_dans_grille(self, x, y):
        """Renvoie True si (x, y) correspond à une case existante (0 à 2)."""
        # On vérifie aussi les nombres NÉGATIFS : en Python, cases[-1]
        # ne plante pas (ça désigne la dernière ligne), donc sans ce test
        # le coup (-1, 0) serait accepté par erreur.
        return 0 <= x <= 2 and 0 <= y <= 2

    def est_libre(self, x, y):
        """Renvoie True si la case est dans la grille ET vide."""
        # Le "and" s'arrête dès que la 1re condition est fausse :
        # on ne lit donc jamais self.cases[x][y] avec un x invalide.
        return self.est_dans_grille(x, y) and self.cases[x][y] == Grille.VIDE

    def jouer(self, x, y, joueur):
        """
        Place le symbole du joueur ("X" ou "O") en (x, y) si c'est possible.
        Renvoie True si le coup est accepté, False s'il est refusé.
        Le booléen renvoyé sert dans la boucle de jeu (partie C) pour
        savoir si le joueur doit rejouer.
        """
        # Cas 1 : coordonnées hors de la grille -> refus
        if not self.est_dans_grille(x, y):
            print(f"Coup refusé : ({x}, {y}) est hors grille.")
            return False
        # Cas 2 : la case contient déjà un symbole -> refus
        if self.cases[x][y] != Grille.VIDE:
            print(f"Coup refusé : la case ({x}, {y}) est occupée.")
            return False
        # Cas 3 : tout est bon, on écrit le symbole dans la case
        self.cases[x][y] = joueur
        return True

    def lignes_gagnantes(self):
        """
        Renvoie la liste des 8 alignements gagnants possibles.
        Chaque alignement est une liste de 3 coordonnées (x, y).
        """
        alignements = []
        # Une seule boucle suffit pour les lignes ET les colonnes :
        for i in range(3):
            # Ligne i : x fixe, y varie -> (i,0) (i,1) (i,2)
            alignements.append([(i, 0), (i, 1), (i, 2)])
            # Colonne i : y fixe, x varie -> (0,i) (1,i) (2,i)
            alignements.append([(0, i), (1, i), (2, i)])
        # Diagonale principale (haut-gauche -> bas-droite)
        alignements.append([(0, 0), (1, 1), (2, 2)])
        # Anti-diagonale (haut-droite -> bas-gauche)
        alignements.append([(0, 2), (1, 1), (2, 0)])
        return alignements  # 3 lignes + 3 colonnes + 2 diagonales = 8

    def est_gagnant(self, j):
        """Renvoie True si le joueur j ("X" ou "O") a aligné 3 symboles."""
        # On teste chacun des 8 alignements.
        for alignement in self.lignes_gagnantes():
            # all(...) vaut True si les 3 cases de l'alignement contiennent j.
            # C'est l'équivalent de :
            #   cases[a] == j and cases[b] == j and cases[c] == j
            if all(self.cases[x][y] == j for x, y in alignement):
                return True   # dès qu'on trouve un alignement, c'est gagné
        return False          # aucun des 8 alignements n'est complet

    def est_plein(self):
        """Renvoie True si plus aucune case n'est libre."""
        for ligne in self.cases:
            # "in" cherche si une case vide existe dans la ligne
            if Grille.VIDE in ligne:
                return False  # il reste au moins une case libre
        return True           # aucune case vide trouvée : grille pleine

    def cases_libres(self):
        """Renvoie la liste des coordonnées (x, y) encore libres."""
        # Compréhension de liste avec double boucle + condition.
        # Utile pour les IA (parties B et bonus).
        return [(x, y) for x in range(3) for y in range(3)
                if self.cases[x][y] == Grille.VIDE]


# Ce bloc ne s'exécute que si on lance CE fichier directement (F5 dans Thonny).
# Il ne s'exécute PAS quand un autre fichier fait "from grille import Grille".
if __name__ == "__main__":
    # ---- Jeu d'essai de l'énoncé ----
    g = Grille()                       # création d'un objet Grille
    g.jouer(0, 0, "X")                 # X en haut à gauche
    g.jouer(0, 1, "O")                 # O en haut au milieu
    g.jouer(1, 1, "X")                 # X au centre
    g.afficher()

    print("jouer(0, 0, 'O')  ->", g.jouer(0, 0, "O"))    # attendu False (occupée)
    print("jouer(3, 0, 'O')  ->", g.jouer(3, 0, "O"))    # attendu False (hors grille)
    print("jouer(-1, 0, 'O') ->", g.jouer(-1, 0, "O"))   # attendu False (hors grille)
    print("est_gagnant('X')  ->", g.est_gagnant("X"))    # attendu False

    g.jouer(2, 2, "X")                 # X complète la diagonale
    print("après jouer(2, 2, 'X') : est_gagnant('X') ->", g.est_gagnant("X"))  # True
    print("est_plein()       ->", g.est_plein())         # attendu False
