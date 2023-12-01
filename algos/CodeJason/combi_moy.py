def appartient(lst, elem):
    """ Renvoie true si elem est dans lst et false sinon"""
    for e in lst :
        if e==elem :
            return True
    return False



def tri_occ (lst):
    """ Trie la liste lst par occurence """

    sous_lst=[]
    taille_sl=[]
    nmb_sl = 0

    for elem in lst :
        i=0

        while i<nmb_sl and appartient(sous_lst[i],elem) :
            i+=1

        if i!=nmb_sl:

            arr=0

            while arr<taille_sl[i] and elem>sous_lst[i][arr]:

                arr+=1

            sous_lst[i].insert(arr,elem)

            taille_sl[i]+=1

        else :
            sous_lst.append([elem])
            nmb_sl+=1
            taille_sl.append(1)

    lst_final=[]

    for sl in sous_lst :
        lst_final=lst_final+sl

    return lst_final



def combi_to_nmb (lst) :
    """Renvois le nombre de carte différentes, doublés, triplés et quadruplé"""
    
    lst_bis=tri_occ(lst)

    lst_coef=[1,0,0,0]
    num_sl=0

    for i in range (1,len(lst)) :
        if lst_bis[i]<=lst_bis[i-1]:
            num_sl+=1
        
        if num_sl<4 :
            lst_coef[num_sl]+=1

    return lst_coef



def nmb_combi_tour (lst, action) :
    """" Renvois le nombre de sous manche de lst """

    nmb_c=combi_to_nmb(lst)
    total=0

    if action[0] :
        total+=nmb_c[0]

    if action[1] :
        total += nmb_c[1] + (nmb_c[0]*(nmb_c[0]-1))/2
    
    if action[2] :
        total += nmb_c[2] + 2* nmb_c[1]*(nmb_c[0]-1) + 3* (nmb_c[0]-1)*nmb_c[0]*(2*nmb_c[0]-4)/12
    
    if action[3] :
        total += nmb_c[3] + 2* nmb_c[2]*(nmb_c[0]-1) + 3* nmb_c[1]*(nmb_c[1]-1)/2 + 4* nmb_c[1]*( (nmb_c[0]-1) * (nmb_c[0]-2)/2) + 6* nmb_c[0]*(nmb_c[0]-1)* (nmb_c[0]*nmb_c[0]-5*nmb_c[0]+6)/24
    
    return total



def sous_manche (main, action) :
    """ Renvoie le nombre de sous manche à partir de main et avec la liste d'action représentée par action"""

    main_tri=tri_occ(main)
    nmb_c=combi_to_nmb(main)
    length=len(main)

    sous_manche=[]

    if action[0] :  # Si on choisit la première action
        for i in range (nmb_c[0]) :
            sous_manche.append([])

            for j in range (length) :
                if j!=i :
                    sous_manche[i].append(main_tri[j])

    if action[1] :  # Si on choisit la deuxième action 
        for i in range (nmb_c[1]) :
            sous_manche.append([])

            for j in range (length) :
                if j+1>nmb_c[0]+nmb_c[1] or main_tri[nmb_c[0]+i]!=main_tri[j] :
                    sous_manche[-1].append(main_tri[j])
        
        for i in range (nmb_c[0]) :
            for l in range (i+1,nmb_c[0]) :

                sous_manche.append([])

                for j in range (length) :
                    if j!=i and j!=l :
                        sous_manche[-1].append(main_tri[j])
    
    if action[2] :  # Dans le cas où on choisit la troisième action

        for i in range (nmb_c[2]) : # Cas où on prend 3 fois la même cartes
            sous_manche.append([])

            for j in range (length) :
                if j+1>nmb_c[0]+nmb_c[1]+nmb_c[2] or main_tri[nmb_c[0]+nmb_c[1]+i]!=main_tri[j]:
                    sous_manche[-1].append(main_tri[j])
        

        for i in range (nmb_c[1]) : # Cas où on prend 2 fois la même carte et une carte différente
            for j in range (nmb_c[0]) :

                if main_tri[i+nmb_c[0]] != main_tri[j] :
                    sous_manche.append([])

                    for c in range (length) :

                        if c!=j and (main_tri[c]!=main_tri[i+nmb_c[0]] or c>nmb_c[0]+nmb_c[1]-1) :
                            sous_manche[-1].append(main_tri[c])

        for i in range (nmb_c[0]) : # Cas où on prend 3 cartes différentes
            for j in range (i+1,nmb_c[0]) :
                for l in range (j+1, nmb_c[0]) :
                    sous_manche.append([])

                    for c in range (length) :
                        if not appartient([i,j,l],c) :
                            sous_manche[-1].append(main_tri[c])

    if action[3] :
        




    print(sous_manche)



main=[0,0,1,3,3,5,6,6,6]
main2 = [0,0,0,2,5,6,6,6,6,6]
#print(tri_occ(main))
#sous_manche(main,[False,False,True,True])
print(tri_occ(main2))
sous_manche(main2,[True,True,True,True])