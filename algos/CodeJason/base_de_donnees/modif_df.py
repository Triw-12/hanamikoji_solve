import pandas as pd

def modif_df(fichier : str,ind_cri : int) :
    """ Modifie la base de donnée correspondant à ind_cri en fonction des données de fichier"""

    #Récupération du critère de réussite
    f = open(fichier, 'r')
    result = int(f.read()[-2])
    f.close


    f = open(fichier, 'r')

    ## Récupération des bases de données
    critere_red = ["M_C","M_P","P","T_C","T_P"]
    critere = ["Manche_Couleurs","Manche_Points","Partie","Tour_Couleurs","Tour_Points"]
    dft = pd.read_csv(critere[ind_cri]+"//donnee"+critere_red[ind_cri]+".csv")
    dfc3 = pd.read_csv(critere[ind_cri]+"//donneechoix3"+critere_red[ind_cri]+".csv")
    dfc4 = pd.read_csv(critere[ind_cri]+"//donneechoix4"+critere_red[ind_cri]+".csv")


    ## Modification des bases de données
    for d in f.readlines() :
        l = d 

        #Enlève les lignes vides et ligne sans information pratique
        if l[0] != '\n' :
            if l[1] == " " :


                l = l.replace(',',';')
                l = l.replace('[','(')
                l = l.replace(']',')')

                m = int(l[0]) + 1
                t = int(l[2]) + 1
                a = int(l[4])


                if a<4 :    # Coup classique
                    c = l[6:9+3*a]
                    cond1 = dft.manche == m
                    cond2 = dft.tour == t
                    cond3 = dft.coup == c

                    if result == 1 :
                        v = dft.loc[ cond1 & cond2 & cond3 , 'nmb_positif']
                        dft.loc[ cond1 & cond2 & cond3 , 'nmb_positif'] = v + result
                    
                    p = dft.loc[ cond1 & cond2 & cond3 , 'nmb_totaux']
                    dft.loc[ cond1 & cond2 & cond3 , 'nmb_totaux'] = p + 1

                elif a == 5 :   #Choix parmis 3
                    c = l[6:15]
                    cond1 = dfc3.manche == m
                    cond2 = dfc3.tour == t
                    cond3 = dfc3.coup == c
                    

                    if result == 1 :
                        pos = "nmb_positif" + str(int(l[16])+1)
                        v = dfc3.loc[ cond1 & cond2 & cond3 , pos]
                        dfc3.loc[ cond1 & cond2 & cond3 , pos] = v + 1
                    
                    tot = "nmb_totaux" + str(int(l[16])+1)
                    p = dfc3.loc[ cond1 & cond2 & cond3 , tot]
                    dfc3.loc[ cond1 & cond2 & cond3 , tot] = p + 1

                else :          #Choix parmis 4
                    c = l[6:18]
                    cond1 = dfc4.manche == m
                    cond2 = dfc4.tour == t
                    cond3 = dfc4.coup == c

                    if result == 1 :
                        pos = "nmb_positif" + str(int(l[19])+1)
                        v = dfc4.loc[ cond1 & cond2 & cond3 , pos]
                        dfc4.loc[ cond1 & cond2 & cond3 , pos] = v + 1
                    
                    tot = "nmb_totaux" + str(int(l[19])+1)
                    p = dfc4.loc[ cond1 & cond2 & cond3 , tot]
                    dfc4.loc[ cond1 & cond2 & cond3 , tot] = p + 1
