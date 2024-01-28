

critère = ["P", "M_C", "M_P", "A_C", "A_P"]




for cri in critère :
    fichier = open("hanamikoji_solve\\algos\\CodeJason\\base_de_donnees\\donnee"+cri+".csv","x")
    fichier.write("manche,tour,nmb_carte,class_par_carte_diff,coup,nmb_positif,nmb_totaux\n")
    for tour in range (3) :
        for manche in range (4) :
            for i in range (8) :
                fichier.write ( str(tour+1) +","+ str(manche+1)+",1,1,("+str(i)+"),0,0\n")

            for i in range (8) :
                for j in range (i+1,8) :
                    fichier.write ( str(tour+1) +","+ str(manche+1)+ ",2,1,("+str(i)+"; "+str(j)+"),0,0\n")

            for i in range (8) :
                fichier.write ( str(tour+1) +","+ str(manche+1)+ ",2,2,("+str(i)+"; "+str(i)+"),0,0\n")


            for i in range (8) :
                for j in range (i+1,8) :
                    for t in range (j+1,8) :
                        fichier.write ( str(tour+1) +","+ str(manche+1)+ ",3,1,("+str(i)+"; "+str(j)+"; "+str(t)+"),0,0\n")
            
            for i in range (8) :
                for j in range (i+1, 8) :
                    fichier.write ( str(tour+1) +","+ str(manche+1)+ ",3,2,("+str(i)+"; "+str(i)+"; "+str(j)+"),0,0\n")
            
            for i in range (8) :
                fichier.write ( str(tour+1) +","+ str(manche+1)+ ",3,3,("+str(i)+"; "+str(i)+"; "+str(i)+"),0,0\n")
            
            for i in range (8) :
                for j in range (i+1, 8) :
                    for t in range (j+1, 8) :
                        for c in range (t+1, 8) :
                            fichier.write ( str(tour+1) +","+ str(manche+1)+ ",4,1,("+str(i)+"; "+str(j)+"; "+str(t)+"; "+str(c)+"),0,0\n")
            
            for i in range (8) :
                for j in range (i+1, 8) :
                    for t in range (j+1, 8) :
                        fichier.write ( str(tour+1) +","+ str(manche+1)+ ",3,2,("+str(i)+"; "+str(i)+"; "+str(j)+"; "+str(t)+"),0,0\n")
            
            for i in range (8) :
                for j in range (i+1, 8) :
                    fichier.write ( str(tour+1) +","+ str(manche+1)+ ",3,2,("+str(i)+"; "+str(i)+"; "+str(j)+"; "+str(j)+"),0,0\n")
            
            for i in range (8) :
                for j in range (i+1, 8) :
                    fichier.write ( str(tour+1) +","+ str(manche+1)+ ",3,2,("+str(i)+"; "+str(i)+"; "+str(i)+"; "+str(j)+"),0,0\n")
                
            for i in range (8) :
                fichier.write ( str(tour+1) +","+ str(manche+1)+ ",3,2,("+str(i)+"; "+str(i)+"; "+str(i)+"; "+str(i)+"),0,0\n")
    fichier.close()
