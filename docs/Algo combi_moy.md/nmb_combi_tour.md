# Nombre de combinaison pour un tour

## Principe

* Calculer le nombre de sous-manches possible à partir d'un tour
* Paramètres: a
  * Action disponible
  * Cartes dans la main
* Utilise le nombre de cartes différentes, doublons, triplés, quadruplés dans la main

## Formules utilisées

* Pour calculer le nombre de combinaison possible, on utilise du dénombrement
  * Soit M une main
  * diff = nombre de cartes différentes de M
  * dou = nombre de doublons dans M
  * tri = nombre de triplés dans M
  * qua = le nombre de quadruplé dans M

    * Pour la chaque action, la formule correspondante est respectivement :
    * $$ Nmbcombi1 = diff $$

    * $$ Nmbcombi2 = doub + {diff \cdot (diff-1) \over 2} $$

    * $$ Nmbcombi3 = tri + 2 \cdot doub \cdot (diff-1) + {doub \cdot (doub-1) \over 2} +3 { (diff-1) \cdot diff \cdot (2 \cdot diff-4) \over 12} $$

    * $$ Nmbcombi4 = quad+2 \cdot trip \cdot (diff-1) +     3 {doub \cdot (doub-1) \over 2 } + 4  {doub \cdot  (diff-1) \cdot (diff-2) \over 2} + 6{ diff \cdot (diff-1) \cdot (diff^2 - 5 \cdot diff +6) \over 24} $$

### Explication des formules

* Dénombrement à faire plus tard
