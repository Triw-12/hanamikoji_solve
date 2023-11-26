# De combinaison à nombre

## Principe
* Renvois une liste comportant le nombre de carte différent, de doublets, de triplets et de quadruplés

## Pseudo-code

* Entrée : une liste L d'éléments
* Sortie : La liste décrit si-dessus

* On suppose la liste en entré triée par occurence et non vide
        
        ind = 0
        Locc <- [1,0,0,0]

        Pour chaque élément c de lst (sauf le
        premier) :

            comparé cette élément avec l'élément 
            précédent, si il est inférieur ou égal 
                ind <- ind+1

            Locc [ind] augmente de 1

        Renvois Locc
