import pandas



fichier= open('hanamikoji_solve\\algos\\CodeJason\\base_de_donnees\\donneeA_C.csv',"r")


df = pandas.read_csv(fichier)

df.loc[0,'nmb_totaux']=3

df.to_csv('hanamikoji_solve\\algos\\CodeJason\\base_de_donnees\\donneeA_C.csv')

fichier.close()