from api import *
from random import *
from time import time

from Pourcent import *
from tab_pourc import tab

MOI = 0
tab_proba = tab()   #importé

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
    t1 = time()

    m = manche()
    t = tour()//2

    main = cartes_en_main()
    main = tri_occ(main)

    action = []
    for i in range (4):
        if not(est_jouee_action(MOI,i)) :
            action.append(True)
        else :
            action.append(False)
    
    coup_c = choix_act(tab_proba,main,action,t,m)
    print(coup_c)

    if coup_c[1]==0 :
        action_valider(coup_c[0][0])

    elif coup_c[1]==1 :
        action_defausser(coup_c[0][0], coup_c[0][1])
    
    elif coup_c[1] == 2 :
        action_choix_trois(coup_c[0][0], coup_c[0][1], coup_c[0][2])

    elif coup_c[1] == 3 :
        action_choix_paquets(coup_c[0][0], coup_c[0][1], coup_c[0][2], coup_c[0][3])
    
    print(coup_c[1]," ",m," ",t," ",coup_c[0])
    print(time()-t1)




# Fonction appelée lors du choix entre les trois cartes lors de l'action de
# l'adversaire (cf tour_precedent)
def repondre_action_choix_trois():
    global tab_proba
    m = manche()
    t = tour()//2

    act_prece = tour_precedent()
    act = [act_prece.c1,act_prece.c2,act_prece.c3]

    choix = choix3(tab_proba,act,t,m)

    repondre_choix_trois(choix)
    print("5 ",m," ",t," ",act)


# Fonction appelée lors du choix entre deux paquet lors de l'action de
# l'adversaire (cf tour_precedent)
def repondre_action_choix_paquets():
    global tab_proba
    m = manche()
    t = tour()//2

    act_prece = tour_precedent()
    act = [act_prece.c1,act_prece.c2,act_prece.c3,act_prece.c4]

    choix = choix4(tab_proba,act,t,m)
    repondre_choix_paquets(choix)
    print("6 ",m," ",t," ",act)


# Fonction appelée à la fin du jeu
def fin_jeu():
    global MOI
    print("fin du jeu")
    nmb_geisha_m = 0
    point_geisha_m = 0
    nmb_geisha_a = 0
    point_geisha_a = 0
    point_g = [2,2,2,3,3,4,5]

    for i in range (7) :
        
        if possession_geisha(i) == MOI :
            nmb_geisha_m+=1
            point_geisha_m += point_g[i]
        elif possession_geisha != 2 :
            nmb_geisha_a+=1
            point_geisha_a += point_g[i]
    
    if point_geisha_m >= 11 :
        print("V")

    elif point_geisha_a >= 11 :
        print("D")
    
    elif nmb_geisha_m >= 4 :
        print("V")

    elif nmb_geisha_a >= 4 :
        print("D")
    
    elif point_geisha_a < point_geisha_m :
        print("V")
    
    elif point_geisha_a > point_geisha_m :
        print("D")
    
    elif nmb_geisha_a < nmb_geisha_m :
        print("V")
    
    elif point_geisha_a > point_geisha_m :
        print("D")
    
    else :
        print("D")
        
