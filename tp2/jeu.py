"""
TP2 R3.08 - Partie C : jeu complet du morpion (+ bonus score et modes).

Ce fichier assemble les parties A et B :
  - la classe Partie gère UNE partie (boucle de jeu, alternance des joueurs,
    validation des coups, détection victoire / nul) ;
  - championnat() enchaîne plusieurs parties et compte le score (bonus) ;
  - main() affiche un menu pour choisir le type de chaque joueur
    (humain, IA, IA maligne) : ça couvre le bonus "mode 2 humains".

Pour jouer : ouvrir ce fichier dans Thonny et appuyer sur F5.
"""

from grille import Grille
from joueurs import JoueurHumain, JoueurIA, JoueurIAMalin


class Partie:
    """Une partie entre deux joueurs : j1 joue X et commence, j2 joue O."""

    def __init__(self, j1, j2, affichage=True):
        # Chaque partie a sa propre grille neuve (composition :
        # une Partie "possède" une Grille).
        self.grille = Grille()
        # Liste de tuples (joueur, symbole) : l'indice 0 joue X, l'indice 1 joue O.
        self.joueurs = [(j1, "X"), (j2, "O")]
        # affichage=False permet de lancer des parties IA vs IA
        # rapidement sans remplir la console (utile pour 20 parties).
        self.affichage = affichage

    def jouer(self):
        """Lance la boucle de jeu. Renvoie le joueur gagnant, ou None si nul."""
        tour = 0   # compteur de tours : sert à savoir à qui c'est le tour
        while True:
            # Alternance des joueurs avec le modulo :
            # tour pair (0, 2, 4...) -> joueurs[0] (X)
            # tour impair (1, 3, 5...) -> joueurs[1] (O)
            joueur, symbole = self.joueurs[tour % 2]

            if self.affichage:
                print()
                self.grille.afficher()
                print(f"\nAu tour de {joueur.nom} ({symbole})")

            # POLYMORPHISME : on ne sait pas si "joueur" est un humain
            # ou une IA, on appelle simplement prochain_coup().
            x, y = joueur.prochain_coup(self.grille.cases, symbole)

            # Validation du coup : grille.jouer() renvoie False si le coup
            # est invalide (et affiche le message d'erreur).
            # Dans ce cas, LE MÊME joueur rejoue (on ne change pas de tour).
            while not self.grille.jouer(x, y, symbole):
                x, y = joueur.prochain_coup(self.grille.cases, symbole)

            # Après un coup valide : est-ce que ce joueur a gagné ?
            if self.grille.est_gagnant(symbole):
                if self.affichage:
                    print()
                    self.grille.afficher()
                    print(f"\n{joueur.nom} ({symbole}) a gagné !")
                return joueur      # fin de partie : on renvoie le gagnant

            # Pas de gagnant mais plus de place : match nul.
            # (On teste la victoire AVANT le nul : si le dernier coup
            # remplit la grille ET fait gagner, c'est une victoire.)
            if self.grille.est_plein():
                if self.affichage:
                    print()
                    self.grille.afficher()
                    print("\nMatch nul !")
                return None        # None = pas de gagnant

            tour += 1              # on passe au joueur suivant


def championnat(j1, j2, nb_parties, affichage=False):
    """
    Bonus : enchaîne nb_parties parties et renvoie le score sous forme
    de dictionnaire {nom_j1: victoires, nom_j2: victoires, "Nuls": nuls}.
    Pour être équitable, les joueurs alternent qui commence (qui a X).
    """
    score = {j1.nom: 0, j2.nom: 0, "Nuls": 0}
    for i in range(nb_parties):
        # Parties paires : j1 commence ; parties impaires : j2 commence
        if i % 2 == 0:
            gagnant = Partie(j1, j2, affichage).jouer()
        else:
            gagnant = Partie(j2, j1, affichage).jouer()

        # Mise à jour du score selon le résultat
        if gagnant is None:
            score["Nuls"] += 1
        else:
            score[gagnant.nom] += 1
    return score


def choisir_joueur(numero):
    """Affiche un menu et renvoie l'objet joueur choisi."""
    while True:   # on redemande tant que le choix est invalide
        print(f"\nJoueur {numero} : 1 = Humain, 2 = IA aléatoire, 3 = IA maligne")
        choix = input("Ton choix : ").strip()   # strip() enlève les espaces
        if choix == "1":
            # "or" : si le nom saisi est vide, on met un nom par défaut
            nom = input("Nom du joueur : ").strip() or f"Joueur {numero}"
            return JoueurHumain(nom)
        if choix == "2":
            return JoueurIA(f"IA {numero}")
        if choix == "3":
            return JoueurIAMalin(f"IA maligne {numero}")
        print("Choix invalide.")


def main():
    """Programme principal : menu, parties successives et score (bonus)."""
    print("=== MORPION ===")
    j1 = choisir_joueur(1)
    j2 = choisir_joueur(2)

    # Score multi-parties (bonus)
    score = {j1.nom: 0, j2.nom: 0, "Nuls": 0}
    premier, second = j1, j2

    while True:
        gagnant = Partie(premier, second).jouer()

        # Expression conditionnelle : clé "Nuls" si pas de gagnant,
        # sinon le nom du gagnant.
        score["Nuls" if gagnant is None else gagnant.nom] += 1
        print("\nScore :", " | ".join(f"{k} : {v}" for k, v in score.items()))

        if input("\nRejouer ? (o/n) : ").strip().lower() != "o":
            break

        # On échange les rôles : celui qui avait O commence la partie suivante
        premier, second = second, premier

    print("Merci d'avoir joué !")


# Point d'entrée : main() ne se lance que si on exécute jeu.py directement
if __name__ == "__main__":
    main()
