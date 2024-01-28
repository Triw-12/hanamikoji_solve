from random import *


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

