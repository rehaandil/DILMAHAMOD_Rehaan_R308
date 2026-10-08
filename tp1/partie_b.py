# TP1 - Partie B 
import random  # import pour tirer des nombres au hasard

rejouer = "o"
while rejouer == "o":  # boucle pour pouvoir rejouer 
    secret = random.randint(1, 100)  # nombre secret entre 1 et 100
    essais = 0
    gagne = False
    print("J'ai choisi un nombre entre 1 et 100. Tu as 10 essais.")

    # sa continue tant qu'il reste des essais et qu'on n'a pas gagné
    while essais < 10 and gagne == False:
        reponse = input("Ton nombre : ")  # input() renvoie toujours du texte
        if not reponse.isdigit():  # si ce n'est pas un nombre, on redemande
            print("Tape un nombre !")
            continue  # retour au début de la boucle, l'essai ne compte pas
        nombre = int(reponse)  # conversion texte a entier
        essais = essais + 1
        if nombre < secret:
            print("Trop petit")
        elif nombre > secret:
            print("Trop grand")
        else:
            print("Gagné en", essais, "essais !")
            gagne = True  # ça arrête la boucle

    if gagne == False:  # on est sorti sans gagner : 10 essais utilisés
        print("Perdu ! Le nombre était", secret)

    rejouer = input("Rejouer ? (o/n) ")