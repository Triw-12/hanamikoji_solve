from random import *
from math import *

from combi_moy import *
from tab_pourc import *

def choix_aleatoire (lst_pourc) :
    """ Renvois aléatoire un indice de lst_pourc, le nombre associé à l'indice est relative à la chance d'obtenir l'indice """
    pourc_tot = 0
    echelle = []
    choix_f = -1


    for choix in lst_pourc :
        pourc_tot += choix
        echelle.append(pourc_tot) 

    num_f = randint(0,pourc_tot-1)

    i = 0
    while choix_f==-1 :
        if echelle[i] > num_f :
            choix_f = i
        i+=1

    return choix_f



def combi_possible(action_j : int, main_tri : list, nmb_combi : int) :
    """Renvois une liste contenant le nombre de carte différente possible à joué"""

    if action_j == 0 :
        return [0]
    
    else :

        lst_combi =[]

        if nmb_combi[action_j] > 0 :
            lst_combi.append(0)

        if nmb_combi[0] > action_j :
            lst_combi.append(action_j)
        
        if action_j == 1:
            return lst_combi
        
        else :
            if nmb_combi[action_j-1] > 0 and nmb_combi[0] > 0 :
                lst_combi.append(1)
        
            if action_j == 2 :
                return lst_combi

            else :
                if (nmb_combi[1] > 0 and nmb_combi[0] > 1) or (nmb_combi[1] > 1) :
                    lst_combi.append(2)
                return lst_combi




def choix_act_dic (Proba: dict, possible: list) :
    """Renvois aléatoire un élément de possible. La chance de chaque élément de possible est contenue dans Proba"""
    list_proba = []

    for coup in possible :
        coup_str = str(coup)
        coup_str = coup_str.replace(',',';')
        coup_str = coup_str.replace('[','(')
        coup_str = coup_str.replace(']',')')
        list_proba.append(Proba.get(coup_str))

    return possible[choix_aleatoire(list_proba)]
        

def choix_act_list (Proba: list, possible: list) :
    """Renvois aléatoire un élément de possible. La chance de chaque élément de possible est contenue dans Proba"""
    list_proba = []

    for coup in possible :
        list_proba.append(Proba[coup][1])

    choisi = possible[choix_aleatoire(list_proba)]
    return choisi
        

def choix_act (Proba: list, main : list, action : list, m : int, t : int) :
    """Lors de la manche m et du tour t, renvois aléatoirement un coup réalisable en fonction de main_tri et action"""
    main_tri = tri_occ(main)
    nmb_combi = combi_to_nmb(main_tri)
    n = len(main_tri)
    tab_eff = Proba[m][t]

    lst_sep = [0]
    for i in range (4) :
        lst_sep.append(lst_sep[i]+nmb_combi[i])

    #Choix parmi les actions possibles
    possible=[]
    for i in range (4) :
        if action[i] :
            possible.append(i)

    action_j = choix_act_list(tab_eff,possible)

    action_j = 3
    #Choix du nombre de cartes
    
    nmb_c_dif_j = combi_possible(action_j,main_tri,nmb_combi)
    
    print(nmb_c_dif_j)
    dif_j = choix_act_list(tab_eff[action_j][0],nmb_c_dif_j)

    print(action_j,dif_j)
    print(nmb_combi)

    #Choix du coup
    coup_possible=[]

    if dif_j == 0 :     # Toutes les cartes sont les mêmes
        for i in range (lst_sep[action_j],lst_sep[action_j+1]) :
            coup = []
            for k in range (action_j+1):
                coup.append(main_tri[i])
            coup_possible.append(tuple(coup))

    elif dif_j == 3 :   #4 cartes sont différentes
        for i in range (nmb_combi[0]) :
            for j in range (i+1,nmb_combi[0]) :
                for r in range (j+1,nmb_combi[0]) :
                    for t in range (r+1,nmb_combi[0]) :
                        coup_possible.append((main_tri[i],main_tri[j],main_tri[r],main_tri[t]))
                        coup_possible.append((main_tri[i],main_tri[r],main_tri[j],main_tri[t]))
                        coup_possible.append((main_tri[i],main_tri[t],main_tri[j],main_tri[r]))

    elif  dif_j == 2 :  #3 cartes sont différentes

        if action_j == 2 :  #On joue 3 cartes au total
            for i in range (nmb_combi[0]) :
                for j in range (i+1,nmb_combi[0]) :
                    for r in range (j+1,nmb_combi[0]) :
                        coup_possible.append((main_tri[i],main_tri[j],main_tri[r]))

        if action_j == 3 :  #On joue 4 cartes au total (ou 2 pair de la même cartes)
            for i in range (nmb_combi[0],nmb_combi[0]+nmb_combi[1]) :    #Cas des pairs
                for j in range (i+1,nmb_combi[0]+nmb_combi[1]) :
                    coup_possible.append((main_tri[i],main_tri[i],main_tri[j],main_tri[j]))
                    coup_possible.append((main_tri[i],main_tri[j],main_tri[i],main_tri[j]))

            for i in range (nmb_combi[0],nmb_combi[0]+nmb_combi[1]) :    #Cas d'une pair
                for j in range (nmb_combi[0]) :
                    if main_tri[i] != main_tri [j] :
                        for r in range (j+1,nmb_combi[0]) :
                            if main_tri[i] != main_tri[r] :
                                coup_possible.append((main_tri[i],main_tri[i],main_tri[j],main_tri[r]))
                                coup_possible.append((main_tri[i],main_tri[j],main_tri[i],main_tri[r]))

    else :  # 2 cartes sont différentes

        if action_j == 1 :  #On joue 2 cartes au total
            for i in range (nmb_combi[0]) :
                for j in range (i+1,nmb_combi[0]) :
                    coup_possible.append((main_tri[i],main_tri[j]))
        
        if action_j == 2 :  #On joue 3 cartes au total
            for i in range (nmb_combi[0],nmb_combi[0]+nmb_combi[1]) :
                for j in range (nmb_combi[0]) :
                    if main_tri[i] != main_tri[j] :
                        coup_possible.append((main_tri[i],main_tri[i],main_tri[j]))
        
        if action_j == 3 : #On joue 4 cartes au total
            for i in range (nmb_combi[0]+nmb_combi[1],nmb_combi[0]+nmb_combi[1]+nmb_combi[2]) :
                for j in range (nmb_combi[0]):
                    if main_tri[i] != main_tri[j] :
                        coup_possible.append((main_tri[i],main_tri[i],main_tri[i],main_tri[j]))
        
    coup_j = choix_act_dic(tab_eff[action_j][0][dif_j][0],coup_possible)

    return coup_j



def choix3 (Proba, coup, t, m) :
    """Renvois le numéro de la carte sélectionnée aléatoirement en fonction des données de Proba"""
    print(coup)
    choix = randint(1,100)
    coup_str = str(coup)

    coup_str = coup_str.replace(",",";")

    proba_coup = Proba[m][t][4][coup_str]

    num = 0
    while choix > 0 :
        choix = choix - proba_coup[num]
        num+=1
    
    return num-1


def choix4 (Proba, coup, t, m) :
    """Renvois le numéro du paquet de cartes sélectionné aléatoirement en fonction des données de Proba"""
    print(coup)
    choix = randint(1,100)
    coup_str = str(coup)

    coup_str = coup_str.replace(",",";")

    proba_coup = Proba[m][t][5][coup_str]

    if choix <= proba_coup[0] :
        return 0
    else :
        return 1



## Test

# tab_proba = tab()
# Proba : dict = {1 : 20, 2 : 10, 3 : 30, 4 : 5, 5 : 35}
# possible : list = [1, 3, 5]

# action = [True,True,True,True]
# main = (5,5,0,4,5,4,4)

# for i in range (50) :
#     print(choix3(tab_proba))
#     print("\n")
