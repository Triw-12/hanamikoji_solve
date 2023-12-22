from api import *
from random import *

MOI = 0

# Fonction appelée au début du jeu
def init_jeu():
    global MOI
    MOI=id_joueur()
    print("debut de la partie")


# Fonction appelée au début du tour
def jouer_tour():
    print("debut du tour")
    global MOI
    n=nb_cartes(MOI)
    main=cartes_en_main()
    non_valid=True

    while non_valid :   #Action choisit aléatoirement
        action_choisie=randint(0,3)
        non_valid=est_jouee_action(MOI,action_choisie)
    
    print("l'action ",action_choisie," a ete selectionne")

    carte_s = []
    for i in range (action_choisie+1) :
        c = randint(0,n-i-1)
        carte_s.append(main.pop(c))

    print ("La (les) carte(s) jouee(s) sont : ", carte_s)

    if action_choisie==0 :
        action_valider(carte_s[0])

    elif action_choisie==1 :
        action_defausser(carte_s[0], carte_s[1])
    
    elif action_choisie == 2 :
        action_choix_trois(carte_s[0], carte_s[1], carte_s[2])

    elif action_choisie == 3 :
        action_choix_paquets(carte_s[0], carte_s[1], carte_s[2], carte_s[3])


# Fonction appelée lors du choix entre les trois cartes lors de l'action de
# l'adversaire (cf tour_precedent)
def repondre_action_choix_trois():
    choix=randint(0,2)
    print("la carte ",choix," a ete selectionne")
    repondre_choix_trois(choix)


# Fonction appelée lors du choix entre deux paquet lors de l'action de
# l'adversaire (cf tour_precedent)
def repondre_action_choix_paquets():
    choix=randint(0,1)
    print("le paquet cartes ",choix," a ete selectionne")
    repondre_choix_paquets(choix)


# Fonction appelée à la fin du jeu
def fin_jeu():
    print("fin du jeu")
