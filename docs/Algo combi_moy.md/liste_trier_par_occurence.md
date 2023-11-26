# Liste trié par occurence

## Principe

Pour une liste L :

* Décomposer L en sous suite dont chaque élément n'est présent qu'une unique fois
* Ces sous-listes doivent être triées dans l'ordre croissant
* La i° sous-liste contient tout les éléments apparraissant i fois dans L
* La liste triée par occurence est la liste obtenu par la concaténation de toute les sous-suites

## Démonstration de validité



## Pseudo-code

* Entré : L une liste à trier
* Sortie: L', la liste obtenu en triant L

        (Lk) <- une suite de liste

        Pour chaque élément e de L:
            Trouver le premier entier k tel que e 
            n'appartient pas à Lk

            insérer e dans Lk (tel que Lk 
            croissant)
        
        L' <- concaténation de tout les Lk
        renvoyer L'