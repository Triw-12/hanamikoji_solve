import csv
import os.path


print(os.listdir('hanamikoji_solve\\algos\\CodeJason\\base_de_donnees')) 
fichier= open('hanamikoji_solve\\algos\\CodeJason\\base_de_donnees\\donneeA_C.csv',"r")

myreader = csv.reader(fichier)

print( csv.get_dialect(myreader))

