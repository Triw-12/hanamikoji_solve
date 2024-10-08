# Règles du jeu Hanamikoji

## Description générale

Le jeu est composé de 7 Geisha et de 21 cartes représentant chacune une Geisha. Il y a 3 Geisha de valeur 2, 2 Geisha de valeur 3, 1 Geisha de valeur 4 et 1 Geisha de valeur 5. La valeur d’une Geisha est aussi le nombre de cartes de cette Geisha disponible (2 cartes pour la Geisha 0, 2 pour la 1, 5 pour la 6…). En effet, les Geisha seront des entiers allant de 0 à 6.

Le jeu se joue en au plus 3 manches (cf conditions de victoires) durant lesquels chaque joueur jouera une et une seule fois chacune des quatre actions (cf actions), qui permettent de valider des cartes. À la fin de chaque manche, pour chaque Geisha, si un joueur a strictement plus de cartes validées que l’adversaire, il prend possession de celle-ci (même si l’adversaire la possédait déjà depuis la manche précédente; au départ les Geisha ne sont possédées par aucun des joueurs).

## Actions

### Valider une carte

Vous validez secrètement une carte en main

### Défausser une carte

Vous défaussez secrètement deux de vos cartes en main, elles sont désormais exclus de la manche.

### Choix trois cartes

Vous choisissez trois cartes de votre main que vous présentez à l’adversaire, celui-ci en choisi une qu’il valide, tandis que vous validez les deux autres.

### Choix paquets

Vous présentez deux paquets de deux cartes de votre main à l’adversaire, il valide le paquet de son choix tandis que vous validez le paquet restant.

Il est alors possible de jouer pendant le tour de l'adversaire pour choisir une ou des cartes que l'adversaire nous propose

Rem : à la fin d'une manche, il y aura alors 8 cartes validées pour chaque joueur

## Déroulement d’une manche

Les cartes sont mélangées, une carte est écartée de la manche, chaque joueur reçoit 6 cartes. Au début de leur tour, les joueurs piochent une carte.

À la fin de la manche, la possession des Geisha est mise à jour : pour chaque Geisha, si un joueur a validé strictement plus de cartes de cette Geisha que l’autre alors il prend possession de celle-ci.

Les conditions de victoires sont vérifiées, s’il n’y a pas de gagnant, on passe à la manche suivante (les possessions des Geisha ne sont pas réinitialisées).

## Conditions de victoires

Un joueur est gagnant dans l’ordre :

* Si la somme des valeurs des Geisha qu’il possède est supérieur ou égal à 11

* S’il possède au moins quatre cartes Geisha

* À la fin des trois manches, la partie s’arrête, le gagnant est celui totalisant le plus grand score (somme des valeurs des Geisha qu’il possède), dans le cas échéant il y a égalité.
