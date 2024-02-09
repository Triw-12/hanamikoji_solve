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
    # Modifie les valeurs de proba en considérant comme proba principal celle d'indice ind avec comme paramètre R réussite et Tc coup totaux
    print(Proba)
    coef = (2*Tc/(R+Tc)) - 1/2
    print(coef)
    n = len(Proba)

    if coef < 1 :
        nouv_Proba= Proba[ind] * coef
    else :
        ecar = (1000 - Proba[ind])/coef
        nouv_Proba = 1000 - ecar

    ecar = Proba[ind] - nouv_Proba
    print(ecar)

    for i in range (n) :
        Proba[i]= ceil(Proba[i] + ecar/(n+1))

    Proba[ind] = ceil(nouv_Proba)

    return Proba

def tab_reussite (df) :
    # Renvoie un tableau dont les cases (final) comporte les données des réussites et des totaux conservé dans df
    lst = []

    for i in range (3) :
        lst.append([])
        for j in range (4) :
            lst.append([])



def modif_1lst(var,reuss) :
    """ Hyppothese : var est soit un tupple contenant un entier entre 1 et 1000 et une liste soit un entier entre 1 et 1000,
        reuss est soit une liste, soit un tupple de 2 entiers
        les listes de reuss et de var doivent être de même taille
    Modifie la probabilité de var ou des valeurs contenues dans var en fonction des données de reuss, renvois le tableau/variable avec les valeurs modifiées"""
    
    if type(var) == int :
        var=nouv_proba (var,reuss[0],reuss[1])
        return (var,reuss[0],reuss[1])
    
    else :
        reu = 0
        tot = 0

        for i in range (var[1].length):
            renvois = modif_1lst(var[1][i],reuss[1][i])

            var[1][i] = renvois[0]
            reu+= renvois[1]
            tot+= renvois[2]

        if var[0] !=100 :
            var[0] = nouv_proba (var[0],reu,tot)

        return var


# def modifie_proba (df,tab) :
#     # Modifie les pourcentages de tab en fonction des données de df
#     tab_r= tab_reussite (df)

#     for case in tab :
#         coup_t = 0
#         for coup in case[1] :
#             diff_t = 0
#             for 


print(nouv_proba([55,132,743,70],2,10,55))