from api import *
import time


def valeur(g, i=False):
    if i and possede(g) != 0:
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


def nb_validee(j, v=False):
    t = 0
    for i in range(7):
        t += nb_cartes_validees(j, i)
    if est_jouee_action(j, action.VALIDER) and v:
        t += 1
    return t


def possede(
    g,
    s=True,
    defausse=[0, 0, 0, 0, 0, 0, 0],
    add_m=[0, 0, 0, 0, 0, 0, 0],
    add_a=[0, 0, 0, 0, 0, 0, 0],
):
    global MOI, ADV, sec
    nb_cartes_jeu = valeur(g)
    nb_cartes_jeu -= defausse[g]
    cartes_v_m = nb_cartes_validees(MOI, g) + add_m[g]
    cartes_v_a = nb_cartes_validees(ADV, g) + add_a[g]
    nb_r_m = 8 - nb_validee(MOI, True)
    nb_r_a = 8 - nb_validee(ADV)
    for i in add_m:
        nb_r_m -= i
    for j in add_a:
        nb_r_a -= j
    diff = cartes_v_m - cartes_v_a
    if s and sec == g:
        cartes_v_m += 1
    majorite = [0, 0]
    if possession_geisha(g) == joueur.EGALITE:
        if nb_cartes_jeu in [0, 1]:
            majorite = [1, 1]
        elif nb_cartes_jeu in [2, 3]:
            majorite = [2, 2]
        else:
            majorite = [3, 3]
    else:
        match nb_cartes_jeu:
            case 0:
                majorite = [0, 1]
            case 1:
                majorite = [1, 1]
            case 2:
                majorite = [1, 2]
            case 3:
                majorite = [2, 2]
            case 4:
                majorite = [2, 3]
            case 5:
                majorite = [3, 3]
        if possession_geisha(g) == ADV:
            majorite[0], majorite[1] = majorite[1], majorite[0]
    if cartes_v_m >= majorite[0]:
        return 1
    elif cartes_v_a >= majorite[1]:
        return -1
    elif nb_r_m + diff < 0 or (nb_r_m + diff == 0 and possession_geisha(g) == ADV):
        print("Special adv")
        return -1
    elif nb_r_a - diff < 0 or (nb_r_a - diff == 0 and possession_geisha(g) == MOI):
        print("Special moi")
        return 1
    else:
        return 0


def possede_bis(
    g,
    s=True,
    defausse=[0, 0, 0, 0, 0, 0, 0],
    add_m=[0, 0, 0, 0, 0, 0, 0],
    add_a=[0, 0, 0, 0, 0, 0, 0],
):
    global MOI, ADV, sec
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
    bis=False,
):
    score = [0, 0]
    if de:
        global defausse
    else:
        defausse = defau
    for i in range(7):
        if bis:
            a = possede_bis(i, s, defausse, add_m, add_a)
        else:
            a = possede(i, s, defausse, add_m, add_a)
        if a == 1:
            score[0] += valeur(i)
        elif a == -1:
            score[1] += valeur(i)
    if score[0] >= 11 and not bis:
        score[0] = 10000
    elif score[1] >= 11 and not bis:
        score[1] = 1000
    return score


MOI = 0
ADV = 0
sec = -1
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


# Fonction appelee au debut du tour
def jouer_tour():
    print("C'est mon tour")
    t1 = time.time()
    global cartes, nb_manche, sec, defausse
    l_cartes = cartes_en_main()
    l_cartes.sort(reverse=True)
    pas_fait = True
    if manche() != nb_manche:
        print("C'est une nouvelle manche")
        sec = -1
        defausse = [0 for _ in range(7)]
        nb_manche = manche()
        cartes = [0 for _ in range(7)]
        for c in l_cartes:
            cartes[c] += 1
    else:
        p = carte_piochee()
        cartes[p] += 1

    if not est_jouee_action(MOI, action.CHOIX_TROIS):
        for i in range(len(cartes)):
            add = [[0 for _ in range(7)] for _ in range(2)]
            add[0][i] += 2
            add[1][i] += 1
            if (
                cartes[i] >= 3
                and possede_bis(i, add_m=add[0], add_a=add[1]) != -1
                and (i != 6 or possession_geisha(i) != -1)
            ):
                cartes[i] -= 3
                e = action_choix_trois(i, i, i)
                print("Triple choix !!")
                pas_fait = False
                break
    # if not est_jouee_action(MOI, action.CHOIX_PAQUETS) and pas_fait:
    #     t = []
    #     for i in range(len(cartes)):
    #         if cartes[i] >= 2 and possession_geisha(i) != ADV:
    #             t.append(i)
    #     while len(t) >= 2 and pas_fait:
    #         add = [[0 for _ in range(7)] for _ in range(2)]
    #         add[0][t[0]] += 1
    #         add[0][t[1]] += 1
    #         add[1][t[0]] += 1
    #         add[1][t[1]] += 1
    #         if possede(t[0], add_m=add[0], add_a=add[1]) == -1:
    #             t.pop(0)
    #         elif possede(t[1], add_m=add[0], add_a=add[1]) == -1:
    #             t.pop(1)
    #         else:
    #             cartes[t[0]] -= 2
    #             cartes[t[1]] -= 2
    #             e = action_choix_paquets(t[0], t[1], t[0], t[1])
    #             print("Deux paquets identiques !")
    #             pas_fait = False
    if not est_jouee_action(MOI, action.DEFAUSSER) and pas_fait:
        for i in range(len(l_cartes)):
            for j in range(i + 1, len(l_cartes)):
                if pas_fait:
                    add = [0, 0, 0, 0, 0, 0, 0]
                    add[l_cartes[i]] += 1
                    add[l_cartes[j]] += 1
                    # print("add (defausse): ", add)
                    if (
                        possede(l_cartes[i], defausse=add) == 1
                        and possede(l_cartes[j], defausse=add) == 1
                        and possede(l_cartes[i]) != 1
                        and possede(l_cartes[i]) != 1
                        and l_cartes[i] != l_cartes[j]
                    ):
                        cartes[l_cartes[i]] -= 1
                        cartes[l_cartes[j]] -= 1
                        e = action_defausser(l_cartes[i], l_cartes[j])
                        print("Defausse tres rentable")
                        pas_fait = False
                        defausse = add
                        break
            if not pas_fait:
                break

    if not est_jouee_action(MOI, action.CHOIX_TROIS) and pas_fait:
        choix_f = []
        score_f = [-1, -1]
        maxi = -1000000
        for i in range(len(l_cartes)):
            for j in range(i + 1, len(l_cartes)):
                for l in range(j + 1, len(l_cartes)):
                    mini = 1000000000
                    for m in range(3):
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
                        res = simul_points(add_m=add_m, add_a=add_a, bis=True)
                        if res[0] - res[1] < mini:
                            mini = res[0] - res[1]
                    if mini > maxi:
                        choix_f = [l_cartes[i], l_cartes[j], l_cartes[l]]
                        score = res
                        maxi = mini

        print("Choix trois par simulation :", score)
        for c in choix_f:
            cartes[c] -= 1
        e = action_choix_trois(choix_f[0], choix_f[1], choix_f[2])
        pas_fait = False
        # for i in range(3):
        #     cartes[l_cartes[i]] -= 1
        # e = action_choix_trois(l_cartes[0], l_cartes[1], l_cartes[2])
        # pas_fait = False
        # print("Choix triple minimum")

    if not est_jouee_action(MOI, action.VALIDER) and pas_fait:
        non = set()
        continuer = True
        while len(non) < 7 and pas_fait and continuer:
            lv = [-1]
            for i in range(len(cartes) - 1, -1, -1):
                if (
                    cartes[i] != 0
                    and possede(i) == 0
                    and valeur(i) > valeur(lv[0])
                    and not (i in non)
                ):
                    lv = [i]
                elif (
                    cartes[i] != 0
                    and possede(i) == 0
                    and valeur(i) == valeur(lv[0])
                    and not (i in non)
                ):
                    lv.append(i)
            if len(lv) == 1 and lv[0] != -1:
                sec = lv[0]
                if possession_geisha(lv[0]) != ADV or possede(lv[0]) == 1:
                    cartes[lv[0]] -= 1
                    e = action_valider(lv[0])
                    print("Je valide !", lv[0])
                    pas_fait = False
                else:
                    print("Cas de validation particulier")
                    non.add(lv[0])
                    sec = -1
            elif len(lv) > 1:
                for c in lv:
                    if (
                        possession_geisha(c) == MOI
                    ):  # Ptetre regarder ses cartes qui restent
                        if cartes[c] == 1:
                            cartes[c] -= 1
                            sec = c
                            e = action_valider(c)
                            print("Je valide !", c)
                            pas_fait = False
                            break
                        else:
                            add = [0, 0, 0, 0, 0, 0, 0]
                            add[l_cartes[i]] += 1
                            add[l_cartes[j]] += 1
                            if (possede(i, defausse=add)) != 1:
                                cartes[c] -= 1
                                sec = c
                                e = action_valider(c)
                                print("Je valide !", c)
                                pas_fait = False
                                break
                if pas_fait:
                    for c in lv:
                        if possession_geisha(c) == joueur.EGALITE:
                            cartes[c] -= 1
                            sec = c
                            e = action_valider(c)
                            print("Je valide !", c)
                            pas_fait = False
                            break
                if pas_fait:
                    for c in lv:
                        sec = c
                        if possede(c) == 1:
                            cartes[c] -= 1
                            e = action_valider(lv[0])
                            print("Je valide !", lv[0])
                            pas_fait = False
                            break
                        else:
                            sec = -1
                            non.add(c)
            else:
                continuer = False
            if pas_fait:
                print("Et c'est parti pour un autre tour")
        if pas_fait:
            print("ATTENTION RECOMMANDE !!!!!!!")
            print(
                "TOUT SEMBLE INUTILE ! Je valide donc la carte la plus haute au hasard"
            )
            for i in range(len(cartes) - 1, -1, -1):
                if cartes[i] != 0:
                    cartes[i] -= 1
                    sec = i
                    e = action_valider(i)
                    pas_fait = False
                    break
    if not est_jouee_action(MOI, action.DEFAUSSER) and pas_fait:
        interessante = -1
        for i in range(len(l_cartes)):
            for j in range(i + 1, len(l_cartes)):
                if pas_fait:
                    add = [0, 0, 0, 0, 0, 0, 0]
                    add[l_cartes[i]] += 1
                    add[l_cartes[j]] += 1
                    if (
                        possede(l_cartes[i], defausse=add) == 1
                        and possede(l_cartes[j], defausse=add) == 1
                    ):
                        cartes[l_cartes[i]] -= 1
                        cartes[l_cartes[j]] -= 1
                        e = action_defausser(l_cartes[i], l_cartes[j])
                        print("Defausse deux cartes identiques ou ininterressante")
                        pas_fait = False
                        defausse = add
                        break
                    elif (
                        possede(l_cartes[j], defausse=add) == 1
                        and possede(l_cartes[j]) != -1
                        and l_cartes[j] > interessante
                    ):
                        interessante = l_cartes[j]
                    elif (
                        possede(l_cartes[i], defausse=add) == 1
                        and possede(l_cartes[i]) != -1
                        and l_cartes[i] > interessante
                    ):
                        interessante = l_cartes[i]
            if not pas_fait:
                break
        if pas_fait and interessante != -1:
            l_cartes.remove(interessante)
            cartes[interessante] -= 1
            cartes[l_cartes[-1]] -= 1  # A ameliorer en fonction de possesion geicha
            defausse[interessante] += 1
            defausse[l_cartes[-1]] += 1
            e = action_defausser(interessante, l_cartes[-1])
            print("Defausse a demi interessante")
            pas_fait = False

    if not est_jouee_action(MOI, action.DEFAUSSER) and pas_fait:
        choix = []
        diff = -10000000
        for i in range(len(l_cartes)):
            for j in range(i + 1, len(l_cartes)):
                add = [0, 0, 0, 0, 0, 0, 0]
                add[l_cartes[i]] += 1
                add[l_cartes[j]] += 1
                res = simul_points(de=False, defau=add)
                if res[0] - res[1] > diff:
                    choix = [l_cartes[i], l_cartes[j]]
                    diff = res[0] - res[1]

        for i in range(2):
            cartes[choix[i]] -= 1
            defausse[choix[i]] += 1
        e = action_defausser(choix[0], choix[1])
        pas_fait = False
        print("Je defausse par simulation (Aie)")
    l_cartes.sort()
    if not est_jouee_action(MOI, action.CHOIX_PAQUETS) and pas_fait:
        maximum = max(cartes)
        if maximum == 3 or maximum == 4:
            for i in range(4):
                cartes[l_cartes[i]] -= 1
            e = action_choix_paquets(l_cartes[0], l_cartes[1], l_cartes[2], l_cartes[3])
            pas_fait = False
            print("Dernier choix de paquets force (sans reel choix)")
        elif maximum == 2:
            num = -1
            for l in range(len(cartes)):
                if cartes[l] == 2:
                    num = l

            liste_d = l_cartes.copy()
            add = [[[0 for _ in range(7)] for _ in range(2)] for _ in range(2)]
            liste_d.remove(num)
            liste_d.remove(num)
            add[1][0][num] += 2
            add[1][1][liste_d[0]] += 1
            add[1][1][liste_d[1]] += 1
            add[0][0][num] += 1
            add[0][1][num] += 1
            add[0][0][liste_d[0]] += 1
            add[0][1][liste_d[1]] += 1
            if possede(
                num, defausse=defausse, add_m=add[0][0], add_a=add[0][1]
            ) == -1 and possede(
                num, defausse=defausse, add_m=add[1][0], add_a=add[1][1]
            ):
                e = action_choix_paquets(num, num, liste_d[0], liste_d[1])
                pas_fait = False
                print("Choix paquets optimal avec 2 / 1-1 ")
            elif possede(num, defausse=defausse, add_m=add[0][0], add_a=add[0][1]) == 1:
                e = action_choix_paquets(num, liste_d[0], num, liste_d[1])
                pas_fait = False
                print("Choix paquets optimal avec 1-1 / 1-1 ")
        else:
            liste_d = l_cartes.copy()
            add = [[[0 for _ in range(7)] for _ in range(2)] for _ in range(3)]
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
        if pas_fait:
            choix_f = []
            maxi = -1000000
            for i in range(len(add)):
                mini = 1000000000
                for j in range(2):
                    l = 1
                    if j == 1:
                        l = 0
                    res = simul_points(add_m=add[i][j], add_a=add[i][l])
                    if res[0] - res[1] < mini:
                        mini = res[0] - res[1]
                if mini > maxi:
                    choix_f = []
                    for p in range(2):
                        for c in range(7):
                            for _ in range(add[i][p][c]):
                                choix_f.append(c)
                    assert len(choix_f) == 4, "Mauvais nombre de cartes"
                    maxi = mini
            e = action_choix_paquets(choix_f[0], choix_f[1], choix_f[2], choix_f[3])
            pas_fait = False
            print("Choix paquets apres simulation")

    if pas_fait:
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
    global nb_manche
    if manche() != nb_manche:
        global cartes, sec, defausse
        l_cartes = cartes_en_main()
        print("C'est une nouvelle manche")
        sec = -1
        defausse = [0 for _ in range(7)]
        nb_manche = manche()
        cartes = [0 for _ in range(7)]
        for c in l_cartes:
            cartes[c] += 1
    print("Repondre action 3")
    choix = []
    maxi = []
    a = tour_precedent()
    lc = [a.c1, a.c2, a.c3]
    for i in range(3):
        maxi.append(lc[i])
        choix.append(i)
    if maxi[0] == maxi[1] and maxi[1] == maxi[2]:
        e = repondre_choix_trois(choix[0])
    else:
        res = []
        choix_m = 0
        diff = -100000
        for l in range(3):
            c = lc.copy()
            # print(c, maxi, l)
            c.remove(maxi[l])
            add_m = [0, 0, 0, 0, 0, 0, 0]
            add_a = [0, 0, 0, 0, 0, 0, 0]
            add_m[maxi[l]] += 1
            add_a[c[0]] += 1
            add_a[c[1]] += 1
            res.append(simul_points(add_m=add_m, add_a=add_a, bis=True))
            if res[l][0] - res[l][1] > diff:
                diff = res[l][0] - res[l][1]
                choix_m = choix[l]
        e = repondre_choix_trois(choix_m)
    print(len(choix), e)
    print()


# Fonction appelee lors du choix entre deux paquets lors de l'action de
# l'adversaire (cf tour_precedent)
def repondre_action_choix_paquets():
    global nb_manche
    if manche() != nb_manche:
        global cartes, sec, defausse
        l_cartes = cartes_en_main()
        print("C'est une nouvelle manche")
        sec = -1
        defausse = [0 for _ in range(7)]
        nb_manche = manche()
        cartes = [0 for _ in range(7)]
        for c in l_cartes:
            cartes[c] += 1
    print("Repondre paquet")
    a = tour_precedent()
    lc = [a.c1, a.c2, a.c3, a.c4]
    if (a.c1 == a.c3 and a.c2 == a.c4) or (a.c1 == a.c4 and a.c2 == a.c3):
        print("Meme paquets !")
        e = repondre_choix_paquets(0)
    else:
        res = []
        choix_m = -1
        diff = -100000
        for l in range(0, 3, 2):
            c = list(lc)
            add_m = [0, 0, 0, 0, 0, 0, 0]
            add_a = [0, 0, 0, 0, 0, 0, 0]
            add_m[c.pop(l)] += 1
            add_m[c.pop(l)] += 1
            add_a[c[0]] += 1
            add_a[c[1]] += 1
            res.append(simul_points(add_m=add_m, add_a=add_a, bis=True))
            i = 0
            if l == 2:
                i = 1
            if res[i][0] - res[i][1] > diff:
                diff = res[i][0] - res[i][1]
                choix_m = i
            elif res[i][0] - res[i][1] == diff:
                choix_m = -1
                print("Egalite")
        print(choix_m)
        if choix_m != -1:
            e = repondre_choix_paquets(choix_m)
        elif valeur(lc[0], True) + valeur(lc[1], True) > valeur(lc[2], True) + valeur(
            lc[3], True
        ):
            print(lc[0], lc[1], lc[2], lc[3], valeur(lc[0]), valeur(lc[2]))
            e = repondre_choix_paquets(0)
        elif valeur(lc[0], True) + valeur(lc[1], True) < valeur(lc[2], True) + valeur(
            lc[3], True
        ):
            print(lc[0], lc[1], lc[2], lc[3], valeur(lc[0]), valeur(lc[2]))
            e = repondre_choix_paquets(1)
        else:
            print("Egalite parfaite")
            if possession_geisha(lc[3]) == MOI or possession_geisha(lc[2]) == MOI:
                e = repondre_choix_paquets(1)
            elif possession_geisha(lc[0]) == MOI or possession_geisha(lc[1]) == MOI:
                e = repondre_choix_paquets(0)
            elif possession_geisha(lc[0]) != ADV and possession_geisha(lc[1]) != ADV:
                e = repondre_choix_paquets(0)
            else:
                e = repondre_choix_paquets(1)  # Au pif
        print("Resultat simulation :", res)
    print("Erreur :", e)
    print()


# Fonction appelee a la fin du jeu
def fin_jeu():
    print("Fin jeu")
