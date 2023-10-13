import itertools as it

a = it.combinations([6,6,5,5,4,2,1],3)
s = set()
for i in a:
    s.add(i)

print(len(s))
print(s)