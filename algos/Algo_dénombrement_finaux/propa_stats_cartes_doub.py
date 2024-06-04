import random as r
from tqdm import tqdm

## On compte le nombre de cartes qui étaient en doublons et qui se retrouvent choisis
max_doubl = [0, 7, 7, 4, 2, 1]
dico = {}
tour_boucle = 100000


def valid(n, nb_simp, nb_doub, nb_trip, nb_quad, nb_quint):
    if n != 5 * nb_quint + 4 * nb_quad + 3 * nb_trip + 2 * nb_doub + nb_simp:
        return False
    if nb_quad > max_doubl[4] - nb_quint:
        return False
    if nb_trip > max_doubl[3] - nb_quad - nb_quint:
        return False
    if nb_doub > max_doubl[2] - nb_quad - nb_quint - nb_trip:
        return False
    if nb_simp > max_doubl[1] - nb_quad - nb_quint - nb_trip - nb_doub:
        return False
    return True


bar = tqdm(total=4319)
for n in range(1, 21):
    for k in range(1, n + 1):
        for nb_simp in range(0, max_doubl[1] + 1):
            for nb_doub in range(0, max_doubl[2] + 1):
                for nb_trip in range(0, max_doubl[3] + 1):
                    for nb_quad in range(0, max_doubl[4] + 1):
                        for nb_quint in range(0, max_doubl[5] + 1):
                            if valid(n, nb_simp, nb_doub, nb_trip, nb_quad, nb_quint):
                                cartes = [nb_simp, nb_doub, nb_trip, nb_quad, nb_quint]
                                comtage = {}
                                for _ in range(tour_boucle):
                                    c = 0
                                    cartes_i = [i for i in range(5)]
                                    count_i = []
                                    for t in range(5):
                                        count_i.append((t + 1) * cartes[t])
                                    choix = r.sample(cartes_i, counts=count_i, k=k)
                                    compte = [0 for _ in range(5)]
                                    for nb in choix:
                                        compte[nb] += 1
                                    cartes_doub = [0 for _ in range(5)]
                                    cartes_doub = tuple(compte)
                                    comtage[cartes_doub] = (
                                        comtage.get(cartes_doub, 0) + 1
                                    )
                                cartes.insert(0, k)
                                cartes.insert(0, n)
                                cartes = tuple(cartes)
                                dico[cartes] = comtage
                                bar.update(1)

fichier = open("stats_cartes_doub.txt", "w")
fichier.write(f"{len(dico)}\n")
for k, v in dico.items():
    fichier.write(f"{k[0]} {k[1]} {k[2]} {k[3]} {k[4]} {k[5]} {k[6]} {len(v)} ")
    for v1, v2 in v.items():
        fichier.write(f"{v1[0]} {v1[1]} {v1[2]} {v1[3]} {v1[4]} {v2} ")
    fichier.write("\n")

print(dico)
