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
    print("10")


## Code
# 10: debut de la partie
# 11: debut du tour
# 12: fin de la partie
# 13: coup joué sans information associé


# Fonction appelée au début du tour
def jouer_tour():
    print("\n11")
    global MOI
    global tab_proba

    m = manche()
    t = tour()//2

    main = cartes_en_main()
    main = tri_occ(main)

    action = []
    for i in range (4):
        
        action.append(not(est_jouee_action(MOI,i)))

    else : 

        coup_c = choix_act(tab_proba,main,action,m,t)

        if coup_c[1]==0 :
            action_valider(coup_c[0][0])

        elif coup_c[1]==1 :
            action_defausser(coup_c[0][0], coup_c[0][1])
        
        elif coup_c[1] == 2 :
            action_choix_trois(coup_c[0][0], coup_c[0][1], coup_c[0][2])

        elif coup_c[1] == 3 :
            action_choix_paquets(coup_c[0][0], coup_c[0][1], coup_c[0][2], coup_c[0][3])
    
        print(m,t,coup_c[1],list(coup_c[0]))




# Fonction appelée lors du choix entre les trois cartes lors de l'action de
# l'adversaire (cf tour_precedent)
def repondre_action_choix_trois():
    global tab_proba
    m = manche()
    t = tour()//2

    act_prece = tour_precedent()
    act = [act_prece.c1,act_prece.c2,act_prece.c3]
    tab_ind = [0,1,2]

    if act[0] == act[1] and act[0] == act[2] :
        repondre_choix_trois(0)
        print("13")

    else :  
        if act[0] == act[2] :
            ech = act[2]
            act[2] = act[1]
            act[1] = ech
            tab_ind[2] = 1
            tab_ind[1] = 2

        elif act[1] == act[2] :
            ech = act[2]
            act[2] = act[0]
            act[0] = ech
            tab_ind[0] = 2
            tab_ind[2] = 0

        elif act[0] != act[1] :
            for i in range(3) :
                for j in range (i+1, 3) :
                    if act[i] > act[j] :
                        ech = act[i]
                        act[i] = act[j]
                        act[j] = ech
                        tab_ind[i] = j
                        tab_ind[j] = i

        choix = choix3(tab_proba,act,m,t)

        repondre_choix_trois(tab_ind[choix])
        print(m,t,"5",act,choix)


# Fonction appelée lors du choix entre deux paquet lors de l'action de
# l'adversaire (cf tour_precedent)
def repondre_action_choix_paquets():
    global tab_proba
    m = manche()
    t = tour()//2

    act_prece = tour_precedent()
    act = [act_prece.c1,act_prece.c2,act_prece.c3,act_prece.c4]

    act1 = [act[0],act[1]]
    act2 = [act[2], act[3]]
    act3 = [act[3],act[2]]

    if (act1 == act2 or act1 == act3) :
        repondre_choix_paquets(0)
        print("13")

    else :
        ech_eff = False

        if act[2] == act[3] :   #Met le paquet doublons comme le premiers paquets
            ech = act[0]
            act[0] = act[2]
            act[2] = ech

            ech = act[1]
            act[1] = act[3]
            act[3] = ech

            ech_eff = True
            
        doubl_paq = act[0] == act[1]
        
        
        doubl_diff = False   
        for i in range (2) :     # Met les doublons des paquets différents en premier de chaque paquet
            for j in range (2) :
                if act[i] == act[2 + j] :
                    doubl_diff = True

                    ech = act[0]
                    act[0] = act[i]
                    act[i] = ech

                    ech = act[2]
                    act[2] = act[2 + j]
                    act[2 + j] = ech


        if doubl_diff and not(doubl_paq) : #Echange dans le cas de premier égaux et second mal placé
            if act[1] > act[3] :
                ech_eff = True

                ech = act[1]
                act[1] = act[3]
                act[3] = ech


        if not (doubl_diff ) :
            for i in range (2) :    #echange les cartes dans un paquet dans le cas d'une mauvaise configuration
                if act[2*i] > act[2*i +1]:
                    ech = act[2*i]
                    act[2*i] = act[2*i +1]
                    act[2*i +1] = ech
                
            if act[0] > act[2] and (not(doubl_paq) or act[2] == act[3]):    #echange les deux paquets
                ech = act[0]
                act[0] = act[2]
                act[2] = ech
                ech = act[1]
                act[1] = act[3]
                act[3] = ech
                ech_eff = True


        choix = choix4(tab_proba,act,m,t)
        if ech_eff :
            repondre_choix_paquets((choix+1) %2)
            print(m,t,"6",act,choix)
        else :
            repondre_choix_paquets(choix)
            print(m,t,"6",act,choix)


# Fonction appelée à la fin du jeu
def fin_jeu():
    global MOI
    print("12")
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
        print("1")

    elif point_geisha_a >= 11 :
        print("0")
    
    elif nmb_geisha_m >= 4 :
        print("1")

    elif nmb_geisha_a >= 4 :
        print("0")
    
    elif point_geisha_a < point_geisha_m :
        print("1")
    
    elif point_geisha_a > point_geisha_m :
        print("0")
    
    elif nmb_geisha_a < nmb_geisha_m :
        print("1")
    
    elif nmb_geisha_a > nmb_geisha_m :
        print("0")
    
    else :
        print("0")
        
