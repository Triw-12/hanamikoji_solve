import itertools as it
import math as m
from tqdm import tqdm

'''
Pour un paquet de cartes donnés, le nombre de combinaisons possibles qui arrive à une solution
'''
cpt = 0
tot = 0
for i in it.permutations(range(1,5),4):
    print(i)
    poss = 6
    nb_cartes = 6
    for l in i:
        nb_cartes += 1
        poss *= m.comb(nb_cartes,l)
        nb_cartes -= l
    assert nb_cartes == 0
    print(poss)
    tot += poss
    cpt += 1

assert cpt == 24
print(tot)
