

critère = ["P", "M_C", "M_P", "T_C", "T_P"]
critère_d = ["Partie","Manche_Couleurs","Manche_Points","Tour_Couleurs","Tour_Points"]
ind= 0


for cri in critère :
    fichier = open("hanamikoji_solve\\algos\\CodeJason\\base_de_donnees\\"+critère_d[ind]+"\\donnee"+cri+".csv","w")
    fichier2 = open("hanamikoji_solve\\algos\\CodeJason\\base_de_donnees\\"+critère_d[ind]+"\\donneechoix3"+cri+".csv","w")
    fichier3 = open("hanamikoji_solve\\algos\\CodeJason\\base_de_donnees\\"+critère_d[ind]+"\\donneechoix4"+cri+".csv","w")
    fichier.write("manche,tour,nmb_carte,class_par_carte_diff,coup,nmb_positif,nmb_totaux\n")
    fichier2.write("manche,tour,coup,nmb_positif1,nmb_totaux1,nmb_positif2,nmb_totaux2,nmb_positif3,nmb_totaux3\n")
    fichier3.write("manche,tour,coup,nmb_positif1,nmb_totaux2,nmb_positif2,nmb_totaux2\n")
    for tour in range (3) :
        for manche in range (4) :
            for i in range (7) :
                fichier.write ( str(tour+1) +","+ str(manche+1)+",1,1,("+str(i)+"),0,0\n")



            for i in range (7) :
                fichier.write ( str(tour+1) +","+ str(manche+1)+ ",2,1,("+str(i)+"; "+str(i)+"),0,0\n")

            for i in range (7) :
                for j in range (i+1,7) :
                    fichier.write ( str(tour+1) +","+ str(manche+1)+ ",2,2,("+str(i)+"; "+str(j)+"),0,0\n")



            for i in range (3,7) :
                fichier.write ( str(tour+1) +","+ str(manche+1)+ ",3,1,("+str(i)+"; "+str(i)+"; "+str(i)+"),0,0\n")

            for i in range (7) :
                for j in range (i+1, 7) :
                    fichier.write ( str(tour+1) +","+ str(manche+1)+ ",3,2,("+str(i)+"; "+str(i)+"; "+str(j)+"),0,0\n")

            for i in range (7) :
                for j in range (i+1,7) :
                    for t in range (j+1,7) :
                        fichier.write ( str(tour+1) +","+ str(manche+1)+ ",3,3,("+str(i)+"; "+str(j)+"; "+str(t)+"),0,0\n")  



            for i in range (5,7) :
                fichier.write ( str(tour+1) +","+ str(manche+1)+ ",4,1,("+str(i)+"; "+str(i)+"; "+str(i)+"; "+str(i)+"),0,0\n")

            for i in range (3,7) :
                for j in range (7) :
                    if j!=i :
                        fichier.write ( str(tour+1) +","+ str(manche+1)+ ",4,2,("+str(i)+"; "+str(i)+"; "+str(i)+"; "+str(j)+"),0,0\n")

            for i in range (7) :
                for j in range (i+1, 7) :
                    fichier.write ( str(tour+1) +","+ str(manche+1)+ ",4,2,("+str(i)+"; "+str(i)+"; "+str(j)+"; "+str(j)+"),0,0\n")
            
            for i in range (7) :
                for j in range (i+1, 7) :
                    for t in range (j+1, 7) :
                        fichier.write ( str(tour+1) +","+ str(manche+1)+ ",4,3,("+str(i)+"; "+str(i)+"; "+str(j)+"; "+str(t)+"),0,0\n")

            for i in range (7) :
                for j in range (i+1, 7) :
                    for t in range (j+1, 7) :
                        for c in range (t+1, 7) :
                            fichier.write ( str(tour+1) +","+ str(manche+1)+ ",4,4,("+str(i)+"; "+str(j)+"; "+str(t)+"; "+str(c)+"),0,0\n")    



            for i in range (7) :
                for j in range (i+1, 7) :
                    fichier2.write ( str(tour+1) +","+ str(manche+1)+ ",("+str(i)+"; "+str(i)+"; "+str(j)+"),0,0,0,0,0,0\n")

            for i in range (7) :
                for j in range (i+1,7) :
                    for t in range (j+1,7) :
                        fichier2.write ( str(tour+1) +","+ str(manche+1)+ ",("+str(i)+"; "+str(j)+"; "+str(t)+"),0,0,0,0,0,0\n") 



            for i in range (3,7) :
                for j in range (7) :
                    if j!=i :
                        fichier3.write ( str(tour+1) +","+ str(manche+1)+ ",("+str(i)+"; "+str(i)+"; "+str(i)+"; "+str(j)+"),0,0,0,0\n")

            for i in range (7) :
                for j in range (i+1,7) :
                        fichier3.write ( str(tour+1) +","+ str(manche+1)+ ",("+str(i)+"; "+str(i)+"; "+str(j)+"; "+str(j)+"),0,0,0,0\n")

            for i in range (7) :
                for j in range (i+1, 7) :
                    for t in range (j+1, 7) :
                        fichier3.write ( str(tour+1) +","+ str(manche+1)+ ",("+str(i)+"; "+str(i)+"; "+str(j)+"; "+str(t)+"),0,0,0,0\n")
                        fichier3.write ( str(tour+1) +","+ str(manche+1)+ ",("+str(i)+"; "+str(j)+"; "+str(i)+"; "+str(t)+"),0,0,0,0\n")

            for i in range (7) :
                for j in range (i+1, 7) :
                    for t in range (j+1, 7) :
                        for c in range (t+1, 7) :
                            fichier3.write ( str(tour+1) +","+ str(manche+1)+ ",("+str(i)+"; "+str(j)+"; "+str(t)+"; "+str(c)+"),0,0,0,0\n")
                            fichier3.write ( str(tour+1) +","+ str(manche+1)+ ",("+str(i)+"; "+str(t)+"; "+str(j)+"; "+str(c)+"),0,0,0,0\n")
                            fichier3.write ( str(tour+1) +","+ str(manche+1)+ ",("+str(i)+"; "+str(c)+"; "+str(j)+"; "+str(t)+"),0,0,0,0\n")  


    fichier.close()
    fichier2.close()
    fichier3.close()
    ind+=1
