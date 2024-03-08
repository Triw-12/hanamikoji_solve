import pandas as pd



df = pd.DataFrame([[0, 2, 3], [0, 4, 1], [10, 20, 30]],index=[4, 5, 6], columns=['A', 'B', 'C'])

dfbis = df[df['A']==0]

for e in dfbis['B'] :
    print(e)

for e in dfbis['C'] :
    print(e)