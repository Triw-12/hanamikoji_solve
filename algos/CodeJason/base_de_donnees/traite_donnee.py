from random import *
from math import *
import pandas as pd

def tab_reussite (ind_cri) :
    # Renvoie un tableau dont les cases (final) comporte les données des réussites et des totaux conservé dans df
    critere = ["Manche_Couleurs","Manche_Points","Partie","Tour_Couleurs","Tour_Points"]
    critere_red = ["M_C","M_P","P","T_C","T_P"]
    tab = []
    dft = pd.read_csv(critere[ind_cri]+"//donnee"+critere_red[ind_cri]+".csv")
    dfc3 = pd.read_csv(critere[ind_cri]+"//donneechoix3"+critere_red[ind_cri]+".csv")
    dfc4 = pd.read_csv(critere[ind_cri]+"//donneechoix4"+critere_red[ind_cri]+".csv")
    crit = ["manche","tour","nmb_carte","class_par_carte_diff"]

    for i in range (3) :    #Par rapport au tour
        dft2 = dft[dft[crit[0]]==i+1]
        dfc3_2 = dfc3[dfc3[crit[0]==i+1]]
        dfc4_2 = dfc4[dfc4[crit[0]==i+1]]
        tab.append([])

        for j in range (4) :    #Par rapport au manche
            dft3 = dft2[dft2[crit[1]]==j+1]
            dfc3_3 = dfc3_2[dfc3_2[crit[0]==i+1]]
            dfc4_3 = dfc4_2[dfc4_2[crit[0]==i+1]]
            tab[i].append([])

            for a in range (4) :    #Par rapport au nombre de carte utilisé
                dft4 = dft3[dft3[crit[2]]==a+1]
                tab[i][j].append([])

                for cd in range (a+1) : #Par rapport au nombre de carte presque différente utilisé
                    dft5 = dft4[dft4[crit[3]]==cd+1]
                    tab[i][j][a].append({})

                    for e in dft5.values :  #Chaque coup
                        tab[i][j][a][cd][e[4]] = (e[5],e[6])
            
            tab[i][j].append({})
            for e in dfc3_3.values :
                tab[i][j][4][e[2]] = (e[3],e[4],e[5],e[6],e[7],e[8])

            tab[i][j].append({})
            for e in dfc4_3.values :
                tab[i][j][5][e[2]] = (e[3],e[4],e[5],e[6])
        

    return tab



def init_proba () :
    """Renvois un tableau de tout les coups avec une probabilité égal pour chaque coup"""
    tab = []
    dft = pd.read_csv("Partie//donneeP.csv")
    dfc3 = pd.read_csv("Partie//donneechoix3P.csv")
    dfc4 = pd.read_csv("Partie//donneechoix4P.csv")
    crit = ["manche","tour","nmb_carte","class_par_carte_diff"]

    for i in range (3) :    #Par rapport au tour
        dft2 = dft[dft[crit[0]]==i+1]
        tab.append([])

        for j in range (4) :    #Par rapport au manche
            dft3 = dft2[dft2[crit[1]]==j+1]
            tab[i].append([])

            for a in range (4) :    #Par rapport au nombre de carte utilisé
                rest1 = 1000-(a+1)*(1000//(a+1))
                dft4 = dft3[dft3[crit[2]]==a+1]
                tab[i][j].append([[],250])

                for cd in range (a+1) : #Par rapport au nombre de carte presque différente utilisé
                    
                    dft5 = dft4[dft4[crit[3]]==cd+1]

                    if rest1 > 0 :
                        tab[i][j][a][0].append([{},1+(1000//(a+1))])
                        rest1 = rest1 -1
                    else :
                        tab[i][j][a][0].append([{},(1000//(a+1))])

                    n = len(dft5)
                    rest2 = 1000-n*(1000//n)

                    for e in dft5.values :  #Chaque coup                        
                        if rest2 >0 :
                            tab[i][j][a][0][cd][0][e[4]] = (1000//n) +1
                            rest2 = rest2 -1
                        else :
                            tab[i][j][a][0][cd][0][e[4]] = (1000//n) 

            #Choix 3
            dfc3_1 = dfc3[dfc3["manche"] == 1]
            dfc3_2 = dfc3_1[dfc3_1["tour"] == 1]
            tab[i][j].append({})
            for e in dfc3_2.values :
                tab[i][j][4][e[2]] = [34,33,33] 
            
            
            #Choix 4
            dfc4_1 = dfc4[dfc4["manche"] == 1]
            dfc4_2 = dfc4_1[dfc4["tour"] == 1]
            tab[i][j].append({})
            for e in dfc4_2 .values :
                tab[i][j][5][e[2]] = [50,50]
    
    return tab



def nouv_proba (Proba:list, ind:int, R:int, Tc:int) :
    """ Hyppothese : la somme des proba vaut 1000, aucune proba ne dépasse 1000 ou passe en dessous de 0, 0<R<Tc, si Tc = 0, la fonction ne fait rien
    Modifie les valeurs de proba en considérant comme proba principal celle d'indice ind avec comme paramètre R réussite et Tc coup totaux"""

    if Tc != 0 :
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



def nouv_proba3 (Proba, lst_reuss) :
    """Modifie les données de proba conformément à lst_reuss"""
    for i in range (3) :
        R = lst_reuss[2*i]
        Tc = lst_reuss[2*i+1]
        if Tc != 0 :
            coef = (R+Tc)/Tc - 0.5

            erreur = 100   #ecard du a l'approximation des pourcentages

            somme = 100 -Proba[i]  #Somme des pourmilles de tout les termes différentes de ind

            if coef < 1 :
                nouv_Proba= Proba[i] * coef
            
                ecar = Proba[i] - nouv_Proba

                for j in range (3) :
                    if j!= i :
                        Proba[j] = ceil(Proba[j] + ecar*(Proba[j]/somme))
                        erreur = erreur - Proba[j]
            
            else :
                nouv_Proba = 100 - (100 - Proba[i])/coef

                ecar = Proba[i] - nouv_Proba

                for j in range (3) :
                    if i!= j :
                        Proba[j] = ceil(Proba[j] + ecar*(Proba[j]/somme))
                        erreur = erreur - Proba[j]
            
            Proba[i] = ceil(nouv_Proba)
            erreur = erreur - Proba[i]

            k =0
            while erreur != 0:
                if erreur < 0 :
                    Proba[k]= Proba[k] - 1
                    erreur+=1
                else :
                    Proba[k]= Proba[k] + 1
                    erreur-=1
                k= (k+1) %3



def nouv_Proba4 (Proba,lst_reuss) :
    for i in range (2) :
        j = (i+1) % 2
        R = lst_reuss[2*i]
        Tc = lst_reuss[2*i+1]
        if Tc != 0 :
            coef = (R+Tc)/Tc - 0.5

            erreur = 100   #ecard du a l'approximation des pourcentages

            somme = 100 -Proba[i]  #Somme des pourmilles de tout les termes différentes de ind

            if coef < 1 :
                nouv_Proba= Proba[i] * coef
            
                ecar = Proba[i] - nouv_Proba


                Proba[j] = ceil(Proba[j] + ecar*(Proba[j]/somme))
                erreur = erreur - Proba[j]
            
            else :
                nouv_Proba = 100 - (100 - Proba[i])/coef

                ecar = Proba[i] - nouv_Proba

                Proba[j] = ceil(Proba[j] + ecar*(Proba[j]/somme))
                erreur = erreur - Proba[j]
            
            Proba[i] = ceil(nouv_Proba)
            erreur = erreur - Proba[i]

            k =0
            while erreur != 0:
                if erreur < 0 :
                    Proba[k]= Proba[k] - 1
                    erreur+=1
                else :
                    Proba[k]= Proba[k] + 1
                    erreur-=1
                k= (k+1) %2



def modif_dico(dico : dict, proba: list) :
    """Modifie le contenue de dico en fonction des donnée de proba"""
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
    """Modifie le contenue des dictionnaires contenues dans lst_dico en fonction de lst_df"""
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
 


def modif_choix3 (dico,dico_reuss) :
    """Modifie les données de dico celon dico_reuss, dico représente des choix avec 3 cas"""
    lst_coup = dico.keys()

    for c in lst_coup :
        nouv_proba3(dico[c],dico_reuss[c])



def modifie_tab (tab, ind_cri) :
    """Hyppothèse: tab est de dimension 3 4"""
    """modifie les probabilité contenue dans tab en fonction des données de df"""

    tab_reuss = tab_reussite(ind_cri)

    for i in range (3) :
        for j in range (4) :
            modif_lst(tab[i][j],tab_reuss[i][j])
            modif_choix3(tab[i][j][4],tab_reuss[i][j][4])



