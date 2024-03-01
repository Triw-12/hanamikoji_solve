from random import *
from math import *

def nouv_proba (Proba:list, ind:int, R:int, Tc:int) :
    """ Hyppothese : la somme des proba vaut 1000, aucune proba ne dépasse 1000 ou passe en dessous de 0, 0<R<Tc
     Modifie les valeurs de proba en considérant comme proba principal celle d'indice ind avec comme paramètre R réussite et Tc coup totaux"""

    coef = (R+Tc)/Tc - 0.5
    n = len(Proba)

    erreur = 1000   #ecard du a l'approximation des pourcentages

    somme = 1000 -Proba[ind][1]  #Somme des pourmilles de tout les termes différentes de ind

    if coef < 1 :
        nouv_Proba= Proba[ind][1] * coef
    
        ecar = Proba[ind][1] - nouv_Proba

        for i in range (n) :
            if i!= ind :
                Proba[i][1] = ceil(Proba[i][1] + ecar*(Proba[i][1]/somme))
                erreur = erreur - Proba[i][1]
    
    else :
        nouv_Proba = 1000 - (1000 - Proba[ind][1])/coef

        ecar = Proba[ind][1] - nouv_Proba

        for i in range (n) :
            if i!= ind :
                Proba[i][1] = ceil(Proba[i][1] + ecar*(Proba[i][1]/somme))
                erreur = erreur - Proba[i][1]

    Proba[ind][1] = ceil(nouv_Proba)
    erreur = erreur - Proba[ind][1]

    i =0
    while erreur != 0:
        if erreur < 0 :
            Proba[i][1]= Proba[i][1] - 1
            erreur+=1
        else :
            Proba[i][1]= Proba[i][1] + 1
            erreur-=1
        i+=1



# def tab_reussite (df) :
#     # Renvoie un tableau dont les cases (final) comporte les données des réussites et des totaux conservé dans df
#     lst = []

#     for i in range (3) :
#         lst.append([])
#         for j in range (4) :
#             lst.append([])

def modif_dico(dico : dict, proba: list) :
    reuss = 0
    tot = 0
    lst_combi = list(dico.items())
    for i in range (len (lst_combi)) :
        lst_combi[i] = list(lst_combi[i])
    for i in range (len(lst_combi)) :
        nouv_proba(lst_combi,i,proba.get(lst_combi[i][0])[0],proba.get(lst_combi[i][0])[1])
        reuss += proba.get(lst_combi[i][0])[0]
        tot += proba.get(lst_combi[i][0])[1]
    dico.update(lst_combi)
    return (reuss,tot)
    


def modif_lst(lst_dico,lst_df) :
    lst_reuss = []
    lst_tot = []
    reuss = 0
    tot = 0
     
    if type(lst_dico) == dict :
        reuss,tot = modif_dico(lst_dico,lst_df)

    else :
        n = len(lst_dico)

        for i in range (n):
            renv = modif_lst(lst_dico[i][0],lst_df[i])
            lst_reuss.append(renv[0])
            lst_tot.append(renv[1])
            reuss += renv[0]
            tot += renv[1]

        for i in range (n):
            nouv_proba(lst_dico,i,lst_reuss[i],lst_tot[i])
    
    return reuss,tot