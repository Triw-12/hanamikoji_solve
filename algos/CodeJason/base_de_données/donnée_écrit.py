

critère = ["P", "M C", "M P", "A C", "A P"]
fichier = open("donnee.csv","a")

for cri in critère :
    for i in range (8) :
        print (cri+", 1, 1, ("+str(i)+")")

    for i in range (8) :
        for j in range (i+1,8) :
            print (cri+ ", 2, 1, ("+str(i)+"; "+str(j)+")")

    for i in range (8) :
        print (cri+ ", 2, 2, ("+str(i)+"; "+str(i)+")")


    for i in range (8) :
        for j in range (i+1,8) :
            for t in range (j+1,8) :
                print (cri+ ", 3, 1, ("+str(i)+"; "+str(j)+"; "+str(t)+")")
    
    for i in range (8) :
        for j in range (i+1, 8) :
            print (cri+ ", 3, 2, ("+str(i)+"; "+str(i)+"; "+str(j)+")")
    
    for i in range (8) :
        print (cri+ ", 3, 3, ("+str(i)+"; "+str(i)+"; "+str(i)+")")
    
    for i in range (8) :
        for j in range (i+1, 8) :
            for t in range (j+1, 8) :
                for c in range (t+1, 8) :
                    