from api import *
import time
from math import inf


def valeur(g, possession=False):
    """
    Renvoie la valeur associé au numéro de la carte objet g
    Le paramètre possession, s'il est égal à True, 
    renvoie une valeur de 0 il est impossible de changer qui à la possession de la geicha
    """
    if possession and possede_abs(g) != 0:
        return 0
    elif g in [0, 1, 2]:
        return 2
    elif g in [3, 4]:
        return 3
    elif g == 5:
        return 4
    elif g == 6:
        return 5
    else:
        return 0


def nouvelle_manche():
    """
    Si une nouvelle manche commence, réinitaliser les variables avec celle de la nouvelle manche
    Renvoie True si c'est une nouvelle manche
    """
    global nb_manche, cartes, sec, defausse
    if manche() != nb_manche:
        print("C'est une nouvelle manche")
        l_cartes = cartes_en_main()
        sec = -1
        defausse = [0 for _ in range(7)]
        nb_manche = manche()
        cartes = [0 for _ in range(7)]
        for c in l_cartes:
            cartes[c] += 1
        return True
    else:
        return False

def nb_validee(j, v=False):
    """
    Compte le nombre total de cartes que le joueur j a déjà validé
    Le paramètre v, s'il est a True, compte une carte de plus si le joueur a déjà joué l'action validé
    """
    t = 0
    for i in range(7):
        t += nb_cartes_validees(j, i)
    if est_jouee_action(j, action.VALIDER) and v:
        t += 1
    return t


def possede_abs(
    g,
    s=True,
    defausse=[0, 0, 0, 0, 0, 0, 0],
    add_m=[0, 0, 0, 0, 0, 0, 0],
    add_a=[0, 0, 0, 0, 0, 0, 0],
):
    """
    Paramètres d'entrées :
    g -> la geicha à tester
    s -> si True, prend en compte la carte secrète si on en a validé une
    defausse -> la défausse à prendre en compte
    add_m -> les cartes que l'on rajoute à soi-même pour faire une simulation
    add_a -> les cartes que l'on rajoute à l'adversaire pour faire une simulation

    Sortie : Renvoie qui va posseder la geicha à la fin de la manche :
    1 -> si c'est moi qui la possède
    -1 -> si c'est l'adversaire
    0 -> si le résultat n'est pas encore définit
    
    """
    global MOI, ADV, sec
    nb_cartes_jeu = valeur(g) - defausse[g]
    cartes_v_m = nb_cartes_validees(MOI, g) + add_m[g] #Mes cartes validées
    cartes_v_a = nb_cartes_validees(ADV, g) + add_a[g] #Les cartes validées par l'adversaires visibles
    nb_r_m = 8 - nb_validee(MOI, True)#Le nombre de cartes que je peux encore valider
    nb_r_a = 8 - nb_validee(ADV)#Le nombre de cartes que l'adversaire peut encore valider (+ sa carte secrète)
    for i in add_m:
        nb_r_m -= i
    for i in add_a:
        nb_r_a -= i
    diff = cartes_v_m - cartes_v_a
    if s and sec == g:
        cartes_v_m += 1
    majorite = [0, 0] #Le nombre de cartes qu'il faut avoir pour obtenir la majorité absolue
    if possession_geisha(g) == joueur.EGALITE:
        if nb_cartes_jeu in [0, 1]:
            majorite = [1, 1]
        elif nb_cartes_jeu in [2, 3]:
            majorite = [2, 2]
        else:
            majorite = [3, 3]
    else:
        tab_maj = [[0, 1],[1, 1],[1, 2],[2, 2],[2, 3],[3, 3]]
        majorite = tab_maj[nb_cartes_jeu]
        if possession_geisha(g) == ADV:#On inverse si c'est l'adversaire qui a la possession
            majorite[0], majorite[1] = majorite[1], majorite[0]
    if cartes_v_m >= majorite[0]:
        return 1
    elif cartes_v_a >= majorite[1]:
        return -1
    elif nb_r_m + diff < 0 or (nb_r_m + diff == 0 and possession_geisha(g) == ADV):#Si je ne peux pas placer assez de cartes pour le dépasser
        print("Special adv")
        return -1
    elif nb_r_a - diff < 0 or (nb_r_a - diff == 0 and possession_geisha(g) == MOI):#S'il ne peut pas placer assez de cartes pour me dépasser
        print("Special moi")
        return 1
    else:
        return 0


def possede_relatif(
    g,
    s=True,
    defausse=[0, 0, 0, 0, 0, 0, 0],
    add_m=[0, 0, 0, 0, 0, 0, 0],
    add_a=[0, 0, 0, 0, 0, 0, 0],
):
    """
    Paramètres d'entrées :
    g -> la geicha à tester
    s -> si True, prend en compte la carte secrète si on en a validé une
    defausse -> la défausse à prendre en compte
    add_m -> les cartes que l'on rajoute à soi-même pour faire une simulation
    add_a -> les cartes que l'on rajoute à l'adversaire pour faire une simulation

    Sortie : Renvoie qui possède la geicha actuellement :
    1 -> si c'est moi qui la possède
    -1 -> si c'est l'adversaire
    0 -> si il y a égalité
    
    """
    global MOI, ADV, sec
    if (possede_abs(g,s,defausse,add_m,add_a) != 0):#Si c'est vrai absolument, on ne regarde même pas relativement
        return possede_abs(g,s,defausse,add_m,add_a)
    cartes_v_m = nb_cartes_validees(MOI, g) + add_m[g]
    cartes_v_a = nb_cartes_validees(ADV, g) + add_a[g]
    if s and sec == g:
        cartes_v_m += 1
    if cartes_v_m > cartes_v_a or (
        cartes_v_m == cartes_v_a and possession_geisha(g) == MOI
    ):
        return 1
    elif cartes_v_m < cartes_v_a or (
        cartes_v_m == cartes_v_a and possession_geisha(g) == ADV
    ):
        return -1
    else:
        return 0


def simul_points(
    s=True,
    de=True,
    add_m=[0, 0, 0, 0, 0, 0, 0],
    add_a=[0, 0, 0, 0, 0, 0, 0],
    defau=[0, 0, 0, 0, 0, 0, 0],
    relatif=False,
):
    """
    Paramètres d'entrées :
    s -> si True, prend en compte la carte secrète si on en a validé une
    de -> si True, prend en compte la defausse
    add_m -> les cartes que l'on rajoute à soi-même pour faire une simulation
    add_a -> les cartes que l'on rajoute à l'adversaire pour faire une simulation
    defau -> la defausse que l'on rajoute pour faire une simulation
    relatif -> si vrai, fait la simulation avec la fonction possede_relatif

    Sortie : Un tableau contenant dans la première case le score que l'on a
    et dans la seconde le score qu'a l'adversaire après simulation
    """
    score = [0, 0]
    if de:
        global defausse
    else:
        defausse = defau
    for i in range(7):
        if relatif:
            a = possede_relatif(i, s, defausse, add_m, add_a)
        else:
            a = possede_abs(i, s, defausse, add_m, add_a)
        if a == 1:
            score[0] += valeur(i)
        elif a == -1:
            score[1] += valeur(i)
    if score[0] >= 11 and not relatif: #Boost de points si on est sûr de gagner
        score[0] = 10000
    elif score[1] >= 11 and not relatif: #Malus de points si on est sûr de perdre 
        score[1] = 1000
    return score


MOI = 0
ADV = 0
sec = -1 #La carte secrete que l'on valide
defausse = [0 for _ in range(7)]
cartes = [0 for _ in range(7)]
nb_manche = -1


# Fonction appelee au debut du jeu
def init_jeu():
    global MOI
    global ADV
    MOI = id_joueur()
    ADV = id_adversaire()
    print(MOI, "debut jeu")


# Fonction appelée au debut du tour
def jouer_tour():
    print("C'est mon tour")
    t1 = time.time()
    global cartes, nb_manche, sec, defausse
    l_cartes = cartes_en_main()
    l_cartes.sort(reverse=True)#Tri des cartes en commencant par la plus forte
    action_non_faite = True

    if not(nouvelle_manche()):
        p = carte_piochee()
        cartes[p] += 1

    #Vérifie si on a 3 cartes identiques
    if not est_jouee_action(MOI, action.CHOIX_TROIS):
        for i in range(len(cartes)):
            add = [[0 for _ in range(7)] for _ in range(2)]
            add[0][i] += 2
            add[1][i] += 1
            if (cartes[i] >= 3):
                cartes[i] -= 3
                e = action_choix_trois(i, i, i)
                print("Triple choix !!")
                action_non_faite = False
                break
    
    #Si on a deux paquets identiques
    if not est_jouee_action(MOI, action.CHOIX_PAQUETS) and action_non_faite:
        t = []
        for i in range(len(cartes)):
            if cartes[i] >= 2 and possession_geisha(i) != ADV:
                t.append(i)
        while len(t) >= 2 and action_non_faite:
            add = [[0 for _ in range(7)] for _ in range(2)]
            add[0][t[0]] += 1
            add[0][t[1]] += 1
            add[1][t[0]] += 1
            add[1][t[1]] += 1
            if possede_abs(t[0], add_m=add[0], add_a=add[1]) == -1:#Vérifie que ça ne fait pas gagner des points à l'adversaire
                t.pop(0)
            elif possede_abs(t[1], add_m=add[0], add_a=add[1]) == -1:
                t.pop(1)
            else:
                cartes[t[0]] -= 2
                cartes[t[1]] -= 2
                e = action_choix_paquets(t[0], t[1], t[0], t[1])
                print("Deux paquets identiques !")
                action_non_faite = False
    
    #Défausse idéale
    if not est_jouee_action(MOI, action.DEFAUSSER) and action_non_faite:
        for i in range(len(l_cartes)):#Pour toutes les permutations de cartes possibles
            for j in range(i + 1, len(l_cartes)):
                if action_non_faite:
                    add = [0, 0, 0, 0, 0, 0, 0]
                    add[l_cartes[i]] += 1
                    add[l_cartes[j]] += 1
                    if (
                        possede_abs(l_cartes[i], defausse=add) == 1
                        and possede_abs(l_cartes[j], defausse=add) == 1
                        and possede_abs(l_cartes[i]) != 1
                        and possede_abs(l_cartes[i]) != 1
                        and l_cartes[i] != l_cartes[j]
                    ):#Si on prend la possession des 2 geichas
                        cartes[l_cartes[i]] -= 1
                        cartes[l_cartes[j]] -= 1
                        e = action_defausser(l_cartes[i], l_cartes[j])
                        print("Defausse tres rentable")
                        action_non_faite = False
                        defausse = add
                        break
            if not action_non_faite:
                break

    # Fait le choix triple en fonction d'un algo min-max partiel
    if not est_jouee_action(MOI, action.CHOIX_TROIS) and action_non_faite:
        choix_f = []
        maxi = -inf
        for i in range(len(l_cartes)):
            for j in range(i + 1, len(l_cartes)):
                for l in range(j + 1, len(l_cartes)):#Pour toutes les permutiations possibles
                    mini = inf
                    for m in range(3):#Pour chaqu'un des placements des cartes
                        #Ajouts des cartes pour simulation
                        add_m = [0 for _ in range(7)]
                        add_a = [0 for _ in range(7)]
                        if m == 0:
                            add_m[l_cartes[i]] += 1
                            add_m[l_cartes[j]] += 1
                            add_a[l_cartes[l]] += 1
                        elif m == 1:
                            add_m[l_cartes[i]] += 1
                            add_a[l_cartes[j]] += 1
                            add_m[l_cartes[l]] += 1
                        else:
                            add_a[l_cartes[i]] += 1
                            add_m[l_cartes[j]] += 1
                            add_m[l_cartes[l]] += 1
                        
                        res = simul_points(add_m=add_m, add_a=add_a, relatif=True)
                        if res[0] - res[1] < mini:#On regarde la pire différence
                            mini = res[0] - res[1]
                    if mini > maxi:#On regarde le meilleur choix parmis toutes les simulations
                        choix_f = [l_cartes[i], l_cartes[j], l_cartes[l]]
                        score = res
                        maxi = mini

        print("Choix trois par simulation :", score)
        for c in choix_f:
            cartes[c] -= 1
        e = action_choix_trois(choix_f[0], choix_f[1], choix_f[2])
        action_non_faite = False

    #Action valider
    if not est_jouee_action(MOI, action.VALIDER) and action_non_faite:
        non = set()
        continuer = True
        while len(non) < 7 and action_non_faite and continuer:
            lv = [-1]
            for i in range(len(cartes) - 1, -1, -1):
                #On regarde toutes ls cartes de mêmes valeurs que l'on possède, que l'on a pas éliminé
                #   et dont la possession est relative 
                if (
                    cartes[i] != 0
                    and possede_abs(i) == 0
                    and valeur(i) > valeur(lv[0])
                    and not (i in non)
                ):
                    lv = [i]
                elif (
                    cartes[i] != 0
                    and possede_abs(i) == 0
                    and valeur(i) == valeur(lv[0])
                    and not (i in non)
                ):
                    lv.append(i)
        
            if len(lv) == 1 and lv[0] != -1:
                sec = lv[0]
                if possession_geisha(lv[0]) != ADV or possede_abs(lv[0]) == 1:
                    #Si elle n'appartient pas à l'adversaire ou que on aura l'avantage après
                    cartes[lv[0]] -= 1
                    e = action_valider(lv[0])
                    print("Je valide !", lv[0])
                    action_non_faite = False
                else:
                    non.add(lv[0])
                    sec = -1
            elif len(lv) > 1: #S'il y en a plusieurs
                for c in lv:
                    if (
                        possession_geisha(c) == MOI
                    ):#On valide en priorité les cartes dont on a l'avantage
                        cartes[c] -= 1
                        sec = c
                        e = action_valider(c)
                        print("Je valide !", c)
                        action_non_faite = False
                        break
                if action_non_faite:
                    for c in lv:
                        if possession_geisha(c) == joueur.EGALITE:
                            #Puis les cartes dont personne n'a d'avantage
                            cartes[c] -= 1
                            sec = c
                            e = action_valider(c)
                            print("Je valide !", c)
                            action_non_faite = False
                            break
                if action_non_faite:
                    for c in lv:
                        sec = c
                        if possede_abs(c) == 1:
                            #Puis si c'est l'adversaire qui a l'avantage et que on est pas sûr de gagner la carte après validation
                            #   On préfereras refaire un autre tour
                            cartes[c] -= 1
                            e = action_valider(lv[0])
                            print("Je valide !", lv[0])
                            action_non_faite = False
                            break
                        else:
                            sec = -1
                            non.add(c)
            else:
                continuer = False
            if action_non_faite:
                print("Et c'est parti pour un autre tour")
        if action_non_faite:#Si toutes les cartes ne semblent pas 'rentables', on valide la plus forte
            for i in range(len(cartes) - 1, -1, -1):
                if cartes[i] != 0:
                    cartes[i] -= 1
                    sec = i
                    e = action_valider(i)
                    action_non_faite = False
                    break
    
    #Action defausser 2
    if not est_jouee_action(MOI, action.DEFAUSSER) and action_non_faite:
        interessante = -1
        for i in range(len(l_cartes)):
            for j in range(i + 1, len(l_cartes)):#Pour toutes les permutations possibles
                if action_non_faite:
                    add = [0, 0, 0, 0, 0, 0, 0]
                    add[l_cartes[i]] += 1
                    add[l_cartes[j]] += 1
                    if (
                        possede_abs(l_cartes[i], defausse=add) == 1
                        and possede_abs(l_cartes[j], defausse=add) == 1
                    ):#Defausse deux cartes identiques ou ininterressantes
                        cartes[l_cartes[i]] -= 1
                        cartes[l_cartes[j]] -= 1
                        e = action_defausser(l_cartes[i], l_cartes[j])
                        action_non_faite = False
                        defausse = add
                        break
                    elif (
                        possede_abs(l_cartes[j], defausse=add) == 1
                        and possede_abs(l_cartes[j]) != -1
                        and l_cartes[j] > interessante
                    ):#On stocke la carte qui nous semble interessante
                        interessante = l_cartes[j]
                    elif (
                        possede_abs(l_cartes[i], defausse=add) == 1
                        and possede_abs(l_cartes[i]) != -1
                        and l_cartes[i] > interessante
                    ):
                        interessante = l_cartes[i]
            if not action_non_faite:
                break
        if action_non_faite and interessante != -1:#Si on en a trouvé une interssante, on la valide avec une autre aléatoire
            l_cartes.remove(interessante)
            cartes[interessante] -= 1
            cartes[l_cartes[-1]] -= 1 
            defausse[interessante] += 1
            defausse[l_cartes[-1]] += 1
            e = action_defausser(interessante, l_cartes[-1])
            print("Defausse a demi interessante")
            action_non_faite = False

    #Defausse 3
    if not est_jouee_action(MOI, action.DEFAUSSER) and action_non_faite:
        choix = []
        diff = -inf
        for i in range(len(l_cartes)):
            for j in range(i + 1, len(l_cartes)):#Toutes les permutations
                add = [0, 0, 0, 0, 0, 0, 0]
                add[l_cartes[i]] += 1
                add[l_cartes[j]] += 1
                res = simul_points(de=False, defau=add)
                if res[0] - res[1] > diff:#On regarde le choix qui nous fait perdre le moins de points
                    choix = [l_cartes[i], l_cartes[j]]
                    diff = res[0] - res[1]

        for i in range(2):
            cartes[choix[i]] -= 1
            defausse[choix[i]] += 1
        e = action_defausser(choix[0], choix[1])
        action_non_faite = False
        print("Je defausse par simulation")

    l_cartes.sort()

    #Choix paquets
    if not est_jouee_action(MOI, action.CHOIX_PAQUETS) and action_non_faite:
        maximum = max(cartes)
        if maximum == 3 or maximum == 4:#On n'a pas le choix
            for i in range(4):
                cartes[l_cartes[i]] -= 1
            e = action_choix_paquets(l_cartes[0], l_cartes[1], l_cartes[2], l_cartes[3])
            action_non_faite = False
            print("Dernier choix de paquets force (sans reel choix)")
        elif maximum == 2:# 2 cartes identiques
            num = -1
            for l in range(len(cartes)):
                if cartes[l] == 2:
                    num = l

            liste_d = l_cartes.copy()
            add = [[[0 for _ in range(7)] for _ in range(2)] for _ in range(2)]#Liste de toutes les possiblités
            liste_d.remove(num)
            liste_d.remove(num)
            #Remplissage de la liste
            add[1][0][num] += 2
            add[1][1][liste_d[0]] += 1
            add[1][1][liste_d[1]] += 1
            add[0][0][num] += 1
            add[0][1][num] += 1
            add[0][0][liste_d[0]] += 1
            add[0][1][liste_d[1]] += 1


            if possede_abs(
                num, defausse=defausse, add_m=add[0][0], add_a=add[0][1]
            ) == -1 and possede_abs(
                num, defausse=defausse, add_m=add[1][0], add_a=add[1][1]
            ):
                e = action_choix_paquets(num, num, liste_d[0], liste_d[1])
                action_non_faite = False
                print("Choix paquets optimal avec les deux identiques du meme cote ")
            elif possede_abs(num, defausse=defausse, add_m=add[0][0], add_a=add[0][1]) == 1:
                e = action_choix_paquets(num, liste_d[0], num, liste_d[1])
                action_non_faite = False
                print("Choix paquets optimal avec les deux identiques dans des paquets differents ")
        else:
            liste_d = l_cartes.copy()
            add = [[[0 for _ in range(7)] for _ in range(2)] for _ in range(3)]
            #Remplissage de la liste
            add[0][0][liste_d[0]] += 1
            add[0][1][liste_d[1]] += 1
            add[0][0][liste_d[2]] += 1
            add[0][1][liste_d[3]] += 1
            add[1][0][liste_d[0]] += 1
            add[1][1][liste_d[2]] += 1
            add[1][0][liste_d[1]] += 1
            add[1][1][liste_d[3]] += 1
            add[2][0][liste_d[0]] += 1
            add[2][1][liste_d[2]] += 1
            add[2][0][liste_d[1]] += 1
            add[2][1][liste_d[3]] += 1
        #Simulation min-max partielle
        if action_non_faite:
            choix_f = []
            maxi = -inf
            for i in range(len(add)):
                mini = inf
                for j in range(2):
                    l = 1 #1 si j = 0; 0 si j = 1
                    if j == 1:
                        l = 0
                    res = simul_points(add_m=add[i][j], add_a=add[i][l])
                    if res[0] - res[1] < mini:
                        mini = res[0] - res[1]
                if mini > maxi:
                    #Ajouts des cartes
                    choix_f = []
                    for p in range(2):
                        for c in range(7):
                            for _ in range(add[i][p][c]):
                                choix_f.append(c)
                    assert len(choix_f) == 4, "Mauvais nombre de cartes"
                    maxi = mini
            e = action_choix_paquets(choix_f[0], choix_f[1], choix_f[2], choix_f[3])
            action_non_faite = False
            print("Choix paquets apres simulation")

    if action_non_faite:
        print("J'ai une erreur, aucune action n'a ete faite")
    elif e != error.OK:
        print("J'ai essayer de faire une action mais j'ai eu l'erreur", e)
    else:
        print("J'ai bien fait mon action en", time.time() - t1)
    print(cartes)
    print()


# Fonction appelee lors du choix entre les trois cartes lors de l'action de
# l'adversaire (cf tour_precedent)
def repondre_action_choix_trois():
    nouvelle_manche()
    print("Repondre action 3")
    choix = []
    maxi = []
    tour_p = tour_precedent()
    lc = [tour_p.c1, tour_p.c2, tour_p.c3]#Liste des cartes possibles
    for i in range(3):
        maxi.append(lc[i])
        choix.append(i)
    if maxi[0] == maxi[1] and maxi[1] == maxi[2]:
        print("Trois cartes identiques")
        e = repondre_choix_trois(choix[0])
    else:
        res = []
        choix_m = 0
        diff = -inf
        for l in range(3):#Pour chaque cartes possibles
            liste_cartes = lc.copy()
            liste_cartes.remove(maxi[l])
            add_m = [0, 0, 0, 0, 0, 0, 0]
            add_a = [0, 0, 0, 0, 0, 0, 0]
            add_m[maxi[l]] += 1
            add_a[liste_cartes[0]] += 1
            add_a[liste_cartes[1]] += 1
            res.append(simul_points(add_m=add_m, add_a=add_a, relatif=True))#Simulations
            if res[l][0] - res[l][1] > diff:
                diff = res[l][0] - res[l][1]
                choix_m = choix[l]
        e = repondre_choix_trois(choix_m)
    print(len(choix), e)
    print()


# Fonction appelee lors du choix entre deux paquets lors de l'action de
# l'adversaire (cf tour_precedent)
def repondre_action_choix_paquets():
    nouvelle_manche()
    print("Repondre paquet")
    tour_p = tour_precedent()
    lc = [tour_p.c1, tour_p.c2, tour_p.c3, tour_p.c4]#Liste des cartes possibles
    if (lc[0] == lc[2] and lc[1] == lc[3]) or (lc[0] == lc[3] and lc[1] == lc[2]):
        print("Meme paquets !")
        e = repondre_choix_paquets(0)
    else:
        res = []
        choix_m = -1
        diff = -inf
        for l in range(0, 3, 2):#l = 0 ou 2
            liste_cartes = list(lc)
            add_m = [0, 0, 0, 0, 0, 0, 0]
            add_a = [0, 0, 0, 0, 0, 0, 0]
            add_m[liste_cartes.pop(l)] += 1#Les deux cartes donnés à l'adversaires (0,1 ou 2,3)
            add_m[liste_cartes.pop(l)] += 1
            add_a[liste_cartes[0]] += 1
            add_a[liste_cartes[1]] += 1
            res.append(simul_points(add_m=add_m, add_a=add_a, relatif=True))
            i = 0
            if l == 2:
                i = 1
            if res[i][0] - res[i][1] > diff:
                diff = res[i][0] - res[i][1]
                choix_m = i
        
        print(choix_m)
        e = repondre_choix_paquets(choix_m)
        print("Resultat simulation :", res)
    print("Erreur :", e)
    print()


# Fonction appelee a la fin du jeu
def fin_jeu():
    print("Fin jeu")
