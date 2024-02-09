from random import *
from math import *

def choix_aleatoire (lst_pourc) :
    pourc_tot = 0
    echelle = []
    choix_f = -1

    for choix in lst_pourc :
        pourc_tot += choix[1]
        echelle.append([choix[0],pourc_tot]) 

    num_f = randint(0,pourc_tot)

    i = 0
    while choix_f==-1 :
        if echelle[i][1] > num_f :
            choix_f = echelle[i][0]
        i+=1

    return choix_f



def nouv_proba (Proba:list, ind:int, R:int, Tc:int) :
    """ Hyppothese : la somme des proba vaut 1000, aucune proba ne dépasse 1000 ou passe en dessous de 0, 0<R<Tc
     Modifie les valeurs de proba en considérant comme proba principal celle d'indice ind avec comme paramètre R réussite et Tc coup totaux"""

    coef = (R+Tc)/Tc - 0.5
    n = len(Proba)

    erreur = 1000   #ecard du a l'approximation des pourcentages

    somme = 1000 -Proba[ind]  #Somme des pourmilles de tout les termes différentes de ind

    if coef < 1 :
        nouv_Proba= Proba[ind] * coef
    
        ecar = Proba[ind] - nouv_Proba

        for i in range (n) :
            if i!= ind :
                Proba[i] = ceil(Proba[i] + ecar*(Proba[i]/somme))
                erreur = erreur - Proba[i]
    
    else :
        nouv_Proba = 1000 - (1000 - Proba[ind])/coef

        ecar = Proba[ind] - nouv_Proba

        for i in range (n) :
            if i!= ind :
                Proba[i] = ceil(Proba[i] + ecar*(Proba[i]/somme))
                erreur = erreur - Proba[i]

    Proba[ind] = ceil(nouv_Proba)
    erreur = erreur - Proba[ind]

    i =0
    while erreur != 0:
        if erreur < 0 :
            Proba[i]= Proba[i] - 1
            erreur+=1
        else :
            Proba[i]= Proba[i] + 1
            erreur-=1
        i+=1



# def tab_reussite (df) :
#     # Renvoie un tableau dont les cases (final) comporte les données des réussites et des totaux conservé dans df
#     lst = []

#     for i in range (3) :
#         lst.append([])
#         for j in range (4) :
#             lst.append([])



def modif_lst(lst_proba,lst_df) :
    lst_reuss = []
    lst_proba = []
    reuss = 0
    tot = 0
     
    if type(lst_proba == dict) :

    else :
        n = len(lst_proba[0])
        
        for i in range (n):
            renv = modif_lst(lst_proba[0][i],lst_df[i])
            lst_reuss.append(renv[0])
            lst_proba.append(lst_proba[0][i][1])
            reuss += renv[0]
            tot += renv[1]

        for i in range (n):
            nouv_proba(lst_proba,i,lst_reuss[i],tot)


# def modifie_proba (df,tab) :
#     # Modifie les pourcentages de tab en fonction des données de df
#     tab_r= tab_reussite (df)

#     for case in tab :
#         coup_t = 0
#         for coup in case[1] :
#             diff_t = 0
#             for 


print(nouv_proba([455,222,173,150],2,15,50))