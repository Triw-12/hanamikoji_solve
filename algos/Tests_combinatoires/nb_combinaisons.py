import itertools as it
import math as m

def C(i1,T1,i2,T2,tour):
    somme = 0
    if tour%2 == 0:
        if 4 in T1:
            T1.remove(4)
            somme += m.comb(i1,4)*6*C(i1-3,T1,i2,T2,tour+1)
            T1.append(4)
        if 3 in T1:
            T1.remove(3)
            somme += m.comb(i1,3)*3*C(i1-2,T1,i2,T2,tour+1)
            T1.append(3)
        if 2 in T1:
            T1.remove(2)
            somme += m.comb(i1,2)*C(i1-1,T1,i2,T2,tour+1)
            T1.append(2)
        if 1 in T1:
            T1.remove(1)
            somme += m.comb(i1,1)*C(i1,T1,i2,T2,tour+1)
            T1.append(1)
    else:
        if 4 in T2:
            T2.remove(4)
            somme += m.comb(i2,4)*6*C(i1,T1,i2-3,T2,tour+1)
            T2.append(4)
        if 3 in T2:
            T2.remove(3)
            somme += m.comb(i2,3)*3*C(i1,T1,i2-2,T2,tour+1)
            T2.append(3)
        if 2 in T2:
            T2.remove(2)
            somme += m.comb(i2,2)*C(i1,T1,i2-1,T2,tour+1)
            T2.append(2)
        if 1 in T2:
            T2.remove(1)
            somme += m.comb(i2,1)*C(i1,T1,i2,T2,tour+1)
            T2.append(1)
    if somme == 0:
        #print(i1,T1,i2,T2,tour)
        return 1
    else :
        return somme


print(C(7,[1,2,3,4],7,[1,2,3,4],0))