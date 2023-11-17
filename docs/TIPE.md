# Résoudre Hanamikoji

Problématique : Peut-t-on trouver une stratégie optimale pour jouer au jeu de société Hanamikoji ?

## Approche

* Règles
* Calculs des différentes combinaisons de choix possible, des différentes combinaisons d’actions possible (en vue de l’algo avec arborescence)
* Différentes stratégies possibles pour les joueurs (4 cartes, 11 points) (théorie de jeux ?)
* Explication de l'api ?
* Algo utilisant des “trics”, des méthodes qui peuvent servir (en utilisant ce qu'il y a avant)
* Algo faisant une arborescence des choix
* Algo qui en sachant les cartes, fait aussi une arborescence des choix et comparaison l’algo précédent

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
* Expliquer le tri des cartes, comment je le stocke et comment il est donné (diff entre l_cartes et cartes)
* Algo min-max partiel (à enlever ?)
* Action valider -> On ne **veux** pas valider les cartes dont on est pas sûr
* Choix optimaux pour le choix paquets, simulation sinon
* Simulation pour le choix 3 cartes et 2 paquets

### Théorie

* Trois cartes identiques -> choix 3 pour empêcher l'adversaire choisir + 2 cartes de mon côté contre 1
* Deux paquets de cartes identiques -> permet à l'adversaire de ne pas faire de choix
* Défausse de deux cartes dont on est sûr d'avoir l'avantage après une défausse ou à défaut une
* Valider en priorité un 5 -> c'est ce qui fait le plus de points
* Sinon, dans la majorité des cas, le plus intéressant est de faire des simulations et de prendre en compte de meilleur score (2 types de modélisations : relatif et absolu) pour tout les choix possibles (dans le cas de choix limités)

### Limites du programme

* 2 paquets de cartes identiques : semble meilleur sans cette fonctionnalité, car facile pour l'adversaire de la déjouer (exemple pour validation de 4 cartes de valeur 5)
* A COMPÉTER

## Algo nombres de combinaisons

### But

On connaît le paquet de cartes et les cartes que on chacun des joueurs et on veut savoir le nombre de combinaisons possibles de faire une manche pour savoir si on peut faire un algo qui regarde qui peut gagner, en sachant l'ensemble du jeu

### Première approche

État sauvegardé :

* La main du joueur 1
* Le nombre d'actions restantes du joueur 1
* La main du joueur 2
* Le nombre d'action restantes du joueur 2
* Le tour
* Le coefficient de multiplication pour avoir une majoration du nombre de noeuds dans le graphe

État pour le graphe :

* La main du joueur 1
* Le nombre d'actions restantes du joueur 1
* La main du joueur 2
* Le nombre d'action restantes du joueur 2
* Les cartes validés et leur position
* Le tour

Tant que la pile est non vide:

* Retirer le dernier élément de la liste*
* Rajouter la carte qu'il a pioché
* Pour toutes les actions possibles restantes:
  * Pour toutes les combinaisons possibles de prendre i cartes (pour la i ème action):
    * Ajouter dans la pile le prochain état possible

Retourne un majorant du nombre de noeuds dans le graphe, le nombre de tour de boucle, et le temps d'execution

### Deuxième approche (Jason)

### Difficultés

* Les doublons qui sont vraiment très compliqué à prendre en compte.

### Conclusion

Impossible de faire cet algorithme (beaucoup trop long) alors que on essaye de jouer en temps réel, donc au max une dizaine de minutes

## Algo déterministe efficace

On connaît et on suit la progression des cartes dans sa main, sur le jeu et celles dont on ne sait pas où elles sont.

* Pour chaque coup que l'on peut jouer:
  * On regarde pour toutes les façons que les cartes ont de finir grâce aux cartes restantes (combinaisons) :
    * Pour chaque état final : on évalue le score des points puis on fait la différence
  * On fait la moyenne pour ce coup
  * On regarde le max des points que l'on a
On joue le coup qui maximise le nombre de points.
