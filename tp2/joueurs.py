"""
TP2 R3.08 - Partie B : classes Joueur (+ bonus JoueurIAMalin).

Principe POO utilisé : l'HÉRITAGE et le POLYMORPHISME.

    Joueur                (classe mère : un nom + prochain_coup())
     ├── JoueurHumain     (choisit son coup au clavier)
     └── JoueurIA         (choisit un coup au hasard)
          └── JoueurIAMalin  (bonus : gagne / bloque / sinon hasard)

Toutes les classes ont la MÊME méthode prochain_coup(tab, symbole)
qui renvoie un tuple (x, y). Grâce à ça, la boucle de jeu (partie C)
peut appeler joueur.prochain_coup(...) sans savoir si c'est un humain
ou une IA : c'est le polymorphisme.
"""

import random                 # module standard, pour random.choice()

from grille import Grille     # on réutilise la classe de la partie A


class Joueur:
    """Classe mère : tout joueur a un nom et sait proposer un coup."""

    def __init__(self, nom):
        # Attribut d'INSTANCE : chaque joueur a son propre nom.
        self.nom = nom

    def prochain_coup(self, tab, symbole):
        """
        tab     : la grille sous forme de liste de listes (grille.cases)
        symbole : "X" ou "O", le symbole de ce joueur
        Renvoie : un tuple (x, y).
        Cette méthode est "abstraite" : elle doit être redéfinie
        dans chaque classe fille. Si on l'appelle sur un Joueur
        de base, on lève une erreur volontairement.
        """
        raise NotImplementedError("À redéfinir dans la classe fille")


class JoueurHumain(Joueur):
    """Joueur qui saisit son coup au clavier.
    (Joueur) entre parenthèses = JoueurHumain HÉRITE de Joueur :
    il récupère automatiquement __init__ et l'attribut nom."""

    def prochain_coup(self, tab, symbole):
        # Boucle infinie : on redemande tant que la saisie n'est pas
        # deux nombres entiers. On sort avec "return".
        while True:
            saisie = input(f"{self.nom} ({symbole}), ton coup 'ligne colonne' (ex : 0 2) : ")

            # On accepte "0 2" et aussi "0,2" : on remplace la virgule
            # par un espace, puis split() découpe sur les espaces.
            morceaux = saisie.replace(",", " ").split()

            # Il faut exactement 2 morceaux (la ligne et la colonne)
            if len(morceaux) != 2:
                print("Il faut deux nombres séparés par un espace.")
                continue          # retour au début de la boucle

            # int() plante (ValueError) si on tape "abc" :
            # on intercepte l'erreur avec try/except pour ne pas planter.
            try:
                x, y = int(morceaux[0]), int(morceaux[1])
            except ValueError:
                print("Saisie invalide : entre des nombres entiers.")
                continue

            # Ici on ne vérifie PAS si la case est libre ou dans la grille :
            # c'est le rôle de Grille.jouer(), appelée par la boucle de jeu.
            # Chaque classe a ainsi une seule responsabilité.
            return x, y


class JoueurIA(Joueur):
    """IA simple : joue un coup aléatoire parmi les cases libres."""

    def prochain_coup(self, tab, symbole):
        # On construit la liste de toutes les cases vides...
        libres = [(x, y) for x in range(3) for y in range(3)
                  if tab[x][y] == Grille.VIDE]
        # ...et on en tire une au hasard.
        # Comme on ne choisit que des cases libres, l'IA ne joue
        # jamais de coup invalide.
        return random.choice(libres)


class JoueurIAMalin(JoueurIA):
    """
    Bonus (mini-jeu 1) : IA un peu plus intelligente.
    Ordre de priorité :
      1) s'il existe un coup qui me fait gagner -> je le joue
      2) sinon, si l'adversaire peut gagner au prochain coup -> je bloque
      3) sinon -> coup au hasard (comportement hérité de JoueurIA)
    Elle hérite de JoueurIA pour pouvoir réutiliser son coup aléatoire.
    """

    def coup_gagnant(self, tab, symbole):
        """
        Cherche une case libre qui, si 'symbole' y jouait, ferait gagner.
        Renvoie (x, y) si elle existe, None sinon.
        """
        # On travaille sur une COPIE de la grille pour ne pas modifier
        # la vraie partie pendant qu'on "essaie" des coups.
        # ligne[:] copie chaque ligne (sinon on copierait juste les références).
        g = Grille()
        g.cases = [ligne[:] for ligne in tab]

        for x, y in g.cases_libres():
            g.cases[x][y] = symbole          # on essaie le coup
            gagne = g.est_gagnant(symbole)   # est-ce que ça gagne ?
            g.cases[x][y] = Grille.VIDE      # on annule le coup d'essai
            if gagne:
                return x, y
        return None                          # aucun coup gagnant trouvé

    def prochain_coup(self, tab, symbole):
        # Le symbole de l'adversaire est l'autre symbole
        adversaire = "O" if symbole == "X" else "X"

        # 1) Est-ce que JE peux gagner tout de suite ?
        coup = self.coup_gagnant(tab, symbole)

        # 2) Sinon, est-ce que L'ADVERSAIRE peut gagner ? Si oui, on se met
        #    sur la case qui le ferait gagner = on le bloque.
        if coup is None:
            coup = self.coup_gagnant(tab, adversaire)

        # 3) Sinon, coup au hasard. super() appelle la méthode de la
        #    classe MÈRE (JoueurIA.prochain_coup) : pas besoin de
        #    réécrire le code du hasard.
        if coup is None:
            coup = super().prochain_coup(tab, symbole)

        return coup


# Tests de la partie B (seulement si on lance ce fichier directement)
if __name__ == "__main__":
    ia = JoueurIA("IA")
    print("JoueurIA sur grille vide ->", ia.prochain_coup(Grille().cases, "X"))

    malin = JoueurIAMalin("Malin")

    # Jeu d'essai 1 de l'énoncé : X X _ / _ O _ / _ _ _ , O joue
    # X menace de gagner en (0, 2) -> O doit bloquer en (0, 2)
    t1 = [["X", "X", " "],
          [" ", "O", " "],
          [" ", " ", " "]]
    print("Bloque :", malin.prochain_coup(t1, "O"))   # attendu (0, 2)

    # Jeu d'essai 2 de l'énoncé : O O _ / X X _ / _ _ _ , O joue
    # O peut gagner en (0, 2) -> gagner passe AVANT bloquer
    t2 = [["O", "O", " "],
          ["X", "X", " "],
          [" ", " ", " "]]
    print("Gagne  :", malin.prochain_coup(t2, "O"))   # attendu (0, 2)
