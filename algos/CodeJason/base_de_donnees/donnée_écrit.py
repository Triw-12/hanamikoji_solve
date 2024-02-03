

critère = ["P", "M_C", "M_P", "T_C", "T_P"]
critère_d = ["Partie","Manche_Couleurs","Manche_Points","Tour_Couleurs","Tour_Points"]
ind= 0


for cri in critère :
    fichier = open("hanamikoji_solve\\algos\\CodeJason\\base_de_donnees\\"+critère_d[ind]+"\\donnee"+cri+".csv","x")
    fichier.write("manche,tour,nmb_carte,class_par_carte_diff,coup,nmb_positif,nmb_totaux\n")
    for tour in range (3) :
        for manche in range (4) :
            for i in range (7) :
                fichier.write ( str(tour+1) +","+ str(manche+1)+",1,1,("+str(i)+"),0,0\n")



            for i in range (7) :
                fichier.write ( str(tour+1) +","+ str(manche+1)+ ",2,1,("+str(i)+"; "+str(i)+"),0,0\n")

            for i in range (7) :
                for j in range (i+1,7) :
                    fichier.write ( str(tour+1) +","+ str(manche+1)+ ",2,2,("+str(i)+"; "+str(j)+"),0,0\n")



            for i in range (7) :
                fichier.write ( str(tour+1) +","+ str(manche+1)+ ",3,1,("+str(i)+"; "+str(i)+"; "+str(i)+"),0,0\n")

            for i in range (7) :
                for j in range (i+1, 7) :
                    fichier.write ( str(tour+1) +","+ str(manche+1)+ ",3,2,("+str(i)+"; "+str(i)+"; "+str(j)+"),0,0\n")

            for i in range (7) :
                for j in range (i+1,7) :
                    for t in range (j+1,7) :
                        fichier.write ( str(tour+1) +","+ str(manche+1)+ ",3,3,("+str(i)+"; "+str(j)+"; "+str(t)+"),0,0\n")  



            for i in range (7) :
                fichier.write ( str(tour+1) +","+ str(manche+1)+ ",4,1,("+str(i)+"; "+str(i)+"; "+str(i)+"; "+str(i)+"),0,0\n")

            for i in range (7) :
                for j in range (i+1, 7) :
                    fichier.write ( str(tour+1) +","+ str(manche+1)+ ",4,2,("+str(i)+"; "+str(i)+"; "+str(i)+"; "+str(j)+"),0,0\n")
            
            for i in range (7) :
                for j in range (i+1, 7) :
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
                    fichier.write ( str(tour+1) +","+ str(manche+1)+ ",-1,1,("+str(i)+"; "+str(i)+"; "+str(j)+"),0,0\n")
                    fichier.write ( str(tour+1) +","+ str(manche+1)+ ",-1,3,("+str(i)+"; "+str(i)+"; "+str(j)+"),0,0\n")

            for i in range (7) :
                for j in range (i+1,7) :
                    for t in range (j+1,7) :
                        fichier.write ( str(tour+1) +","+ str(manche+1)+ ",-1,1,("+str(i)+"; "+str(j)+"; "+str(t)+"),0,0\n") 
                        fichier.write ( str(tour+1) +","+ str(manche+1)+ ",-1,2,("+str(i)+"; "+str(j)+"; "+str(t)+"),0,0\n")  
                        fichier.write ( str(tour+1) +","+ str(manche+1)+ ",-1,3,("+str(i)+"; "+str(j)+"; "+str(t)+"),0,0\n")  



            for i in range (7) :
                for j in range (i+1, 7) :
                    fichier.write ( str(tour+1) +","+ str(manche+1)+ ",-2,1,("+str(i)+"; "+str(i)+"; "+str(i)+"; "+str(j)+"),0,0\n")

            for i in range (7) :
                for j in range (i+1, 7) :
                    for t in range (j+1, 7) :
                        fichier.write ( str(tour+1) +","+ str(manche+1)+ ",-2,1,("+str(i)+"; "+str(i)+"; "+str(j)+"; "+str(t)+"),0,0\n")
                        fichier.write ( str(tour+1) +","+ str(manche+1)+ ",-2,1,("+str(i)+"; "+str(j)+"; "+str(i)+"; "+str(t)+"),0,0\n")

            for i in range (7) :
                for j in range (i+1, 7) :
                    for t in range (j+1, 7) :
                        for c in range (t+1, 7) :
                            fichier.write ( str(tour+1) +","+ str(manche+1)+ ",-2,1,("+str(i)+"; "+str(j)+"; "+str(t)+"; "+str(c)+"),0,0\n")
                            fichier.write ( str(tour+1) +","+ str(manche+1)+ ",-2,1,("+str(i)+"; "+str(t)+"; "+str(j)+"; "+str(c)+"),0,0\n")
                            fichier.write ( str(tour+1) +","+ str(manche+1)+ ",-2,1,("+str(i)+"; "+str(c)+"; "+str(j)+"; "+str(t)+"),0,0\n")  


    fichier.close()
    ind+=1
