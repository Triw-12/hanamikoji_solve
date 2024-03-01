from random import *
from math import *

from combi_moy import *

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



def choix_act_dic (Proba: dict, possible: list) :
    """Renvois aléatoire un élément de possible. La chance de chaque élément de possible est contenue dans Proba"""
    list_proba = []
    for coup in possible :
        list_proba.append(Proba.get(coup))
    return possible[choix_aleatoire(list_proba)]
        

def choix_act_list (Proba: list, possible: list) :
    """Renvois aléatoire un élément de possible. La chance de chaque élément de possible est contenue dans Proba"""
    list_proba = []
    for coup in possible :
        list_proba.append(Proba[coup][1])
    choisi = possible[choix_aleatoire(list_proba)]
    return choisi
        

def choix_act (Proba: list, main : list, action : list, t : int, m : int) :
    """Lors de la manche m et du tour t, renvois aléatoirement un coup réalisable en fonction de main et action"""
    tri_occ(main)
    list_combi = combi_to_nmb(main)
    n = len(main)
    tab_eff = Proba[t][m]

    action_j = choix_act_list(tab_eff,action)

    nmb_c_dif_j = []
    for i in range (action_j) :
        if list_combi[i]!=0 and list_combi[0]>=action_j-i :
            nmb_c_dif_j.append(True)
        else :
            nmb_c_dif_j.append(False)
    
    dif_j = choix_act_list(tab_eff[action_j],nmb_c_dif_j)

    coup_possible=[]

    if dif_j == 0 :
        for i in range (list_combi[action_j],list_combi[action_j+1]) :
            coup = []
            for k in range (action_j):
                coup.append(main[i])
            coup_possible.append(coup)

    elif dif_j == 3 :
        
        
       
        














    
    



