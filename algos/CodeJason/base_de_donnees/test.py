def modif(d) :
    lst_d = list(d.items())
    for i in range (4) :
        lst_d[i] = (i,i)
    print(lst_d)
    d.update(lst_d)
    
    

d = {0 : 3, 1 : 4, 2 : 10, 3 : 0}
f =(1,0)
print((1,0)[1])
print(d)
modif(d)
print(d)

print(type([3,2]))