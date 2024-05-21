import pandas as pd

f = open("test_donnée.txt", 'r')

result = int(f.read()[-2])


f.close


f = open("test_donnée.txt", 'r')
dft = pd.read_csv("test_resulte.csv")
dft2 = pd.read_csv("test_resulte2.csv")
dft3 = pd.read_csv("test_resulte3.csv")

for d in f.readlines() :
    l = d 
    if l[0] != '\n' :
        if l[1] == " " :
            l = l.replace(',',';')
            l = l.replace('[','(')
            l = l.replace(']',')')

            m = int(l[0])
            t = int(l[2])
            a = int(l[4])

            cond1 = dft.manche == m
            cond2 = dft.tour == t

            if a<5 :
                c = l[6:9+3*a]
                cond3 = dft.coup == c

                if result == 1 :
                    v = dft.loc[ cond1 & cond2 & cond3 , 'nmb_positif']
                    dft.loc[ cond1 & cond2 & cond3 , 'nmb_positif'] = v + result
                
                p = dft.loc[ cond1 & cond2 & cond3 , 'nmb_totaux']
                dft.loc[ cond1 & cond2 & cond3 , 'nmb_totaux'] = p + 1

            elif a == 5 :
                c = l[6:15]
                cond3 = dft.coup == c
                

                if result == 1 :
                    pos = "nmb_positif" + str(int(l[16])+1)
                    v = dft2.loc[ cond1 & cond2 & cond3 , pos]
                    dft2.loc[ cond1 & cond2 & cond3 , pos] = v + 1
                
                tot = "nmb_totaux" + str(int(l[16])+1)
                p = dft2.loc[ cond1 & cond2 & cond3 , tot]
                dft2.loc[ cond1 & cond2 & cond3 , tot] = p + 1

            else :
                c = l[6:18]
                cond3 = dft.coup == c

                if result == 1 :
                    pos = "nmb_positif" + str(int(l[19])+1)
                    v = dft3.loc[ cond1 & cond2 & cond3 , pos]
                    dft3.loc[ cond1 & cond2 & cond3 , pos] = v + 1
                
                tot = "nmb_totaux" + str(int(l[19])+1)
                p = dft3.loc[ cond1 & cond2 & cond3 , tot]
                dft3.loc[ cond1 & cond2 & cond3 , tot] = p + 1


            





dft.to_csv('test_resulte.csv', sep = ',', index = False)

