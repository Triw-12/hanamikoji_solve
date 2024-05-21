f = open("test_donnée.txt", 'r')

result = int(f.read()[-2])


f.close

if result == 1 :
    f = open("test_donnée.txt", 'r')

    for d in f.readlines() :
        l = d 
        if l[0] != '\n' :
            if l[1] == " " :
                l = l.replace(',',';')
                l = l.replace('[','(')
                l = l.replace(']',')')
                
                