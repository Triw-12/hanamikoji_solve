from api import *
from random import *

from Pourcent import *

MOI = 0
tab_proba = []#importé

# Fonction appelée au début du jeu
def init_jeu():
    global MOI
    global tab_proba
    MOI=id_joueur()
    print("debut de la partie")



# Fonction appelée au début du tour
def jouer_tour():
    print("debut du tour")
    global MOI
    global tab_proba

    m = manche()
    t = tour()//2
    n=nb_cartes(MOI)

    main=cartes_en_main()
    main = tri_occ(main)
    non_valid=True

    action = [False,False,False,False]
    for i in range (4):
        action[i] = est_jouee_action(MOI,action.i)
    
    coup_c = choix_act(tab_proba,main,action,t,m)

    if coup_c[1]==0 :
        action_valider(coup_c[0][1])

    elif coup_c[1]==1 :
        action_defausser(coup_c[0][1], coup_c[0][3])
    
    elif coup_c[1] == 2 :
        action_choix_trois(coup_c[0][1], coup_c[0][3], coup_c[0][5])

    elif coup_c[1] == 3 :
        action_choix_paquets(coup_c[0][1], coup_c[0][3], coup_c[0][5], coup_c[0][7])




# Fonction appelée lors du choix entre les trois cartes lors de l'action de
# l'adversaire (cf tour_precedent)
def repondre_action_choix_trois():
    act = tour_precedent()
    


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
