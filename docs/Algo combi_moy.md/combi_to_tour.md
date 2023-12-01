# De combinaison aux nombres de doublons

## Principe

* Renvoie une liste comportant le nombre de cartes différentes, de doublets, de triplets et de quadruplés

## Pseudo-code

* Entrée : une liste L d'éléments
* Sortie : La liste décrit si-dessus

* On suppose la liste en entré triée par occurrence et non vide

```text
    ind <- 0
    Locc <- [1,0,0,0] #Liste triée par occurrence

    Pour chaque élément c de lst (sauf le
    premier) :

        comparer cet élément avec l'élément précédent, si il est inférieur ou égal alors :
            ind <- ind+1

        Locc[ind] += 1

    Renvoie Locc
```
