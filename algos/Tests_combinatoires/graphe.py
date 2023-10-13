import itertools as it
paquets = [5,5,5,3,3,3,6,6,6,6,6,0,5,0,1,2,1,2,4,4,4]


def possiblite(p,n):
    a = it.combinations(p,n)
    s = set()
    for i in a:
        s.add(i)
    return s
print(paquets[6:12])

def C():
    cpt = 0
    pile = [[paquets[:6],paquets[6:12],set([1,2,3,4]),set([1,2,3,4]),12,1]]
    while len(pile) != 0:
        if len(pile)%40 == 0:
            print(len(pile))
        etat = pile.pop()
        P1 =  etat[0]
        P2 = etat[1]
        T1 = etat[2]
        T2 = etat[3]
        tour = etat[4]
        cst = etat[5]#NE PAS OUBLIER DE METTRE CST A JOUR
        if tour == 20:
            pass
        elif tour%2 == 0:
            P1.append(paquets[tour])
            for i in T1:
                a = possiblite(P1,i)
                for p in a:
                    P1suiv = P1.copy()
                    T1suiv = T1.copy()
                    T1suiv.remove(i)
                    for carte in p:
                        P1suiv.remove(carte)
                    pile.append([P1suiv,P2,T1suiv,T2,tour+1,cst])
                    cpt += cst
        else:
            P2.append(paquets[tour])
            for i in T2:
                a = possiblite(P2,i)
                for p in a:
                    P2suiv = P2.copy()
                    T2suiv = T2.copy()
                    T2suiv.remove(i)
                    for carte in p:
                        P2suiv.remove(carte)
                    pile.append([P1,P2suiv,T1,T2suiv,tour+1,cst])
                    cpt += cst
    return cpt

print(C())






# a = it.combinations([0,0,4,4,4,2],4)
# s = set()
# for i in a:
#     s.add(i)

# print(len(s))
# print(s)