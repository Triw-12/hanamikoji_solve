import itertools as it
from tqdm import tqdm
import os
paquets = [5,5,5,3,3,3,6,6,6,6,6,0,5,0,1,2,1,2,4,4,4]


def possiblite(p,n):
    a = it.combinations(p,n)
    s = set()
    for i in a:
        s.add(i)
    return s
print(paquets[6:12])

def C():
    if os.path.exists("save_graphe.txt"):
        print("Récupération du fichier en cours")
        fichier = open("save_graphe.txt","r")
        cpt = int(fichier.readline().strip())
        tour_boucle = int(fichier.readline().strip())
        nb_pile = int(fichier.readline().strip())
        pile = []
        for _ in range(nb_pile):
            etat = []
            for _ in range(2):
                p1 = fichier.readline().strip().split(" ")
                for elem in range(len(p1)):
                    p1[elem] = int(p1[elem])
                etat.append(p1)
            for _ in range(2):
                p1 = fichier.readline().strip().split(" ")
                s1 = set()
                for elem in range(len(p1)):
                    try:
                        s1.add(int(p1[elem]))
                    except:
                        print(p1)
                        exit()
                etat.append(s1)
            etat.append(int(fichier.readline().strip()))
            etat.append(int(fichier.readline().strip()))
            pile.append(etat)
        print("Récupération du fichier terminé")
    else:
        pbar = tqdm(total=229249440000)
        tour_boucle = 0
        cpt = 0
        pile = [[paquets[:6],paquets[6:12],set([1,2,3,4]),set([1,2,3,4]),12,1]]
    while len(pile) != 0:
        if tour_boucle%100000 == 0:
            print(tour_boucle,len(pile))
        etat = pile.pop()
        p1 =  etat[0]
        p2 = etat[1]
        t1 = etat[2]
        t2 = etat[3]
        tour = etat[4]
        cst = etat[5]
        if tour == 20:
            pass
        elif tour%2 == 0:
            p1.append(paquets[tour])
            for i in t1:
                a = possiblite(p1,i)
                for p in a:
                    p1suiv = p1.copy()
                    t1suiv = t1.copy()
                    t1suiv.remove(i)
                    for carte in p:
                        p1suiv.remove(carte)
                    cst1 = cst
                    if i == 3:
                        cst1 *= 3
                    if i ==  4:
                        cst1 *= 6
                    assert len(p1suiv) <= 7, (p1suiv, p1,tour_boucle,p)
                    pile.append([p1suiv,p2,t1suiv,t2,tour+1,cst1])
                    cpt += cst1
        else:
            p2.append(paquets[tour])
            for i in t2:
                a = possiblite(p2,i)
                for p in a:
                    p2suiv = p2.copy()
                    t2suiv = t2.copy()
                    t2suiv.remove(i)
                    for carte in p:
                        p2suiv.remove(carte)
                    cst2 = cst
                    if i == 3:
                        cst2 *= 3
                    if i ==  4:
                        cst2 *= 6
                    assert len(p1) <= 7, p1
                    pile.append([p1,p2suiv,t1,t2suiv,tour+1,cst2])
                    cpt += cst2
        tour_boucle += 1
        pbar.update(1)
        if tour_boucle%1000000 == 0:
            print("Sauvegarde en cours...")
            print(pile)
            fichier = open("save_graphe.txt","w")
            fichier.write(str(cpt) + "\n")
            fichier.write(str(tour_boucle) + "\n")
            fichier.write(str(len(pile)) + "\n")
            for etat_p in pile:
                for l in range(4):
                    for p1_c in etat_p[l]:
                        fichier.write(str(p1_c) + " ")
                    fichier.write("\n")
                fichier.write(f"{etat_p[4]}\n{etat_p[5]}\n")
            fichier.close()
            print("Sauvegarde terminée")

            
    pbar.close()
    return cpt

print(C())


