# Liste triée par occurrence

## Principe

Pour une liste L :

* Décomposer L en suite de listes dont chaque élément n'est présent qu'une seule fois
* Ces listes doivent être triées dans l'ordre croissant
* La i° liste contient tout les éléments apparaissant i fois dans L
* La liste triée par occurrence est la liste obtenue par la concaténation de toutes les listes de la suite

## Démonstration de validité

A COMPÉTER

## Pseudo-code

* Entrée : L une liste à trier
* Sortie: L' la liste obtenue en triant L

```text
    (Lk) <- une suite de listes

    Pour chaque élément e de L:
        Trouver le premier entier k tel que e 
        n'appartient pas à Lk

        insérer e dans Lk (tel que Lk 
        croissant)
    
    L' <- concaténation de tout les Lk
    renvoyer L'
```
