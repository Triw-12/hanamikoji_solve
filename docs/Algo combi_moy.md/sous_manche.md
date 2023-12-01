# Sous manche

## Principe

* Renvoie toutes les sous-manches possibles
* Paramètres :
  * Une main de cartes
  * Les actions disponibles

## Pseudo-code

* Pour ce code, on sépare les différentes sous manches en 4 catégories:
  * Les sous manches engendrées par la première action
  * Les sous manches engendrées par la deuxième action
  * Les sous manches engendrées pas la troisième action
  * Les sous manches engendrées par la quatrième action

* On suppose la liste de cartes prise en entrée triée par occurrence
* On se permet aussi d'utiliser les différents nombres obtenues par la fonction combi_to_nmb
* On se permet de définir 4 sépare-main, représentant les 4 sections du trie par occurrence

* Pour le premier set de sous-manches :
  * Pour chaque  
