# Résoudre Hanamikoji

Problématique : Peut-t-on trouver une stratégie optimale pour jouer au jeu de société Hanamikoji ?

## Approche

* Règles
* Calculs des différentes combinaisons de choix possible, des différentes combinaisons d’actions possible (en vue de l’algo avec arborescence)
* Différentes stratégies possibles pour les joueurs (4 cartes, 11 points) (théorie de jeux ?)
* Expliquation de l'api ?
* Algo utilisant des “trics”, des méthodes qui peuvent servir (en utilisant ce qu'il y a avant)
* Algo faisant une arborescence des choix
* Algo qui en sachant les cartes, fait aussi une arborescence des choix et comparaison l’algo précédent

## Modélisation


Modéliser le jeu (cf API)


## Combinaisons

### Combinaisons de cartes

* 21 cartes (1 carte défaussé dès le début)
* Au départ : 6 cartes par personnes puis on pioche une cartes à chaque tour
* Répartitions des cartes : 5 de valeur 5, 4 de valeur 4, 2\* 3 de valeur 3, 3\* 2 de valeur 2

### Combinaisons d'actions

* Nombres d’actions : 4
* 1 action prenant 1 carte, 1 action prenant 2 cartes, 1 action prenant 3 cartes, 1 action prenant 4 cartes

## Explication de l'algo normal

### Dans le code
* Tableau pour la majorité
* Cas spéciaux pour la possession de Geisha -> en fonction des cartes que je peux encore valider
* Expliquer le tri des cartes, comment je le stocke et comment il est donné
* Algo min-max partiel (à enlever ?)
* Action valider -> On ne veux pas valider les cartes dont on est pas sur
* Choix optimaux pour le choix paquets

### Théorie (à enlever ?)
* Trois cartes identiques -> choix 3 pour empêcher l'adversaire choisir + 2 cartes de mon côté contre 1
* Deux paquets de cartes identiques -> premet à l'adversaire de ne pas faire de choix
* Défausse de deux cartes dont on est sûr d'avoir l'avantage après une défausse ou à défaut une
* Valider en priorité un 5 -> c'est ce qui fait le plus de points
* Sinon, dans la majorité des cas, le plus interessant est de faire des simulations et de prendre en compte de meilleur score (2 types de modélisations : relatif et absolu) pour tout les choix possibles (dans le cas de choix limités

## Algo suivant les graphes

A venir (voir cours ?)
