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

    lst=lst_final



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



# def nmb_combi_tour (lst, action) :
#     """" Renvois le nombre de sous manche de lst """

#     nmb_c=combi_to_nmb(lst)
#     total=0

#     if action[0] :
#         total +=nmb_c[0]

#     if action[1] :
#         total += nmb_c[1] + (nmb_c[0]*(nmb_c[0]-1))/2
    
#     if action[2] :
#         total += nmb_c[2] + 2* nmb_c[1]*(nmb_c[0]-1) + 3* (nmb_c[0]-1)*nmb_c[0]*(2*nmb_c[0]-4)/12
    
#     if action[3] :
#         total += nmb_c[3] + 2* nmb_c[2]*(nmb_c[0]-1) + 3* nmb_c[1]*(nmb_c[1]-1)/2 + 4* nmb_c[1]*( (nmb_c[0]-1) * (nmb_c[0]-2)/2) + 6* nmb_c[0]*(nmb_c[0]-1)* (nmb_c[0]*nmb_c[0]-5*nmb_c[0]+6)/24
    
#     return total



def sous_manche (main, action) :
    """ Renvoie les sous manche à partir de main et avec la liste d'action représentée par action"""

    main_tri=tri_occ(main)
    nmb_c=combi_to_nmb(main)
    length=len(main)

    sous_manche=[[],[],[[],[],[]],[[],[],[],[],[]]]

    if action[0] :      # Si on choisit la première action
        for i in range (nmb_c[0]) :
            sous_manche[0].append([])

            for j in range (length) :
                if j!=i :
                    sous_manche[0][i].append(main_tri[j])



    if action[1] :      # Si on choisit la deuxième action 
        for i in range (nmb_c[1]) :     # 2 fois la même carte
            sous_manche[1].append([])

            for j in range (length) :
                if j+1>nmb_c[0]+nmb_c[1] or main_tri[nmb_c[0]+i]!=main_tri[j] :
                    sous_manche[1][-1].append(main_tri[j])
        

        for i in range (nmb_c[0]) :     # 2 cartes différentes
            for l in range (i+1,nmb_c[0]) :

                sous_manche[1].append([])

                for j in range (length) :
                    if j!=i and j!=l :
                        sous_manche[1][-1].append(main_tri[j])
    


    if action[2] :      # Si on choisit la troisième action

        for i in range (nmb_c[2]) :     # 3 fois la même cartes
            sous_manche[2][0].append([])
            

            for j in range (length) :
                if j+1>nmb_c[0]+nmb_c[1]+nmb_c[2] or main_tri[nmb_c[0]+nmb_c[1]+i]!=main_tri[j]:
                    sous_manche[2][0][-1].append(main_tri[j])
        

        for i in range (nmb_c[1]) :     # 2 fois la même carte et une carte différente
            for j in range (nmb_c[0]) :

                if main_tri[i+nmb_c[0]] != main_tri[j] :
                    sous_manche[2][1].append([])

                    for c in range (length) :

                        if c!=j and (main_tri[c]!=main_tri[i+nmb_c[0]] or c>nmb_c[0]+nmb_c[1]-1) :
                            sous_manche[2][1][-1].append(main_tri[c])


        for i in range (nmb_c[0]) :     # 3 cartes différentes
            for j in range (i+1,nmb_c[0]) :
                for l in range (j+1, nmb_c[0]) :
                    sous_manche[2][2].append([])

                    for c in range (length) :
                        if not appartient([i,j,l],c) :
                            sous_manche[2][2][-1].append(main_tri[c])



    if action[3] :      # Si on choisit la 4e action
        nmb_a3=nmb_c[0]+nmb_c[1]+nmb_c[2]


        for i in range (nmb_c[3]) :     # 4 fois la même carte
            sous_manche[3][0].append([])

            for c in range (length) :

                if main_tri[c]!=main_tri[i+nmb_a3] or c>=nmb_a3+nmb_c[3] :
                    sous_manche[3][0][-1].append(main_tri[c])


        for i in range (nmb_c[2]) :     # 3 fois la même carte et 1 carte différente

            for j in range (nmb_c[0]) :

                if main_tri[j] != main_tri[i+nmb_c[0]+nmb_c[1]] :
                    sous_manche[3][1].append([])

                    for c in range (length) :

                        if c != j and (main_tri[c] != main_tri[nmb_c[0]+nmb_c[1]+i] or c>=nmb_a3) :
                            sous_manche[3][1][-1].append(main_tri[c])

        for i in range (nmb_c[1]) :     # 2 paires différentes de 2 fois la même carte 
            for j in range (i+1, nmb_c[1]) :
                sous_manche[3][2].append([])

                for c in range (length) :

                    if (c>=nmb_c[0]+nmb_c[1] or not(appartient ([main_tri[i+nmb_c[0]],main_tri[j+nmb_c[0]]],main_tri[c]))) :
                        sous_manche[3][2][-1].append(main_tri[c])
        
        for i in range (nmb_c[1]) :     # 2 fois la même carte et 2 cartes différentes

            for j in range (nmb_c[0]) :
                for l in range (j+1, nmb_c[0]) :

                    if main_tri[i+nmb_c[0]]!=main_tri[j] and main_tri[i+nmb_c[0]]!=main_tri[l] :
                        sous_manche[3][3].append([])

                        for c in range (length) :

                            if c!=l and c!=j and (c>=nmb_c[0]+nmb_c[1] or main_tri[c]!=main_tri[i+nmb_c[0]]) :
                                sous_manche[3][3][-1].append(main_tri[c])
        
        for i in range (nmb_c[0]) :     # 4 cartes différentes
            for j in range (i+1,nmb_c[0]) :
                for l in range (j+1,nmb_c[0]) :
                    for k in range (l+1,nmb_c[0]) :
                        sous_manche[3][4].append([])

                        for c in range (length) :
                            
                            if not(appartient([i,j,l,k], c)) :
                                sous_manche[3][4][-1].append(main_tri[c])

    return sous_manche

def nmb_moy(main, deck, action) :
    """Renvois le nombre de combinaison total sur une partie commenceant par main et deck, avec les actions disponible dans action"""

    if action==[False,False,False,False] :
        return 1

    nouv_deck=deck [:]
    nouv_main=(main+ [nouv_deck.pop()]) [:]

    renvois=0
    ss_m=sous_manche(nouv_main,action)

    for i in range (2) :
        
        nouv_action=action[:]

        for lst in ss_m[i] :
            nouv_action[i]=False

            if action==[False,False,False,False] :
                return 1

            renvois += nmb_moy(lst,nouv_deck,nouv_action)
        
    nouv_action=action[:]
    nouv_action[2]=False

    for i in range (3) :
        for lst in ss_m[2][i] :
            renvois += (i+1)* nmb_moy(lst,nouv_deck,nouv_action)

    nouv_action=action[:]
    nouv_action[3]=False

    for i in range (5) :
        for lst in ss_m[3][i] :
            renvois += (1+i+i//5) * nmb_moy(lst,nouv_deck,nouv_action)

    return renvois






# main=[0,0,1,3,3,5,6,6,6]
# main2 = [0,0,0,2,5,6,6,0,6,6]
# print(tri_occ(main))
# print(sous_manche(main,[False,False,False,True]))
# print(tri_occ(main2))
# print(sous_manche(main2,[False,False,False,True]))

sm = sous_manche ([1,2,3,4,5,6,7],[True,False,False,False])

for ssm in sm :
    for m in ssm :
        print("G ou P, 1, 1, ",m)


#print(nmb_combi_tour([5,5,5,4,4,2],[True,True,True,True]))