# Nombre de combianaison pour un tour

## Principe

* Calculer le nombre de sous-manche possible à partir d'un tour
* paramètre: action disponible, carte dans la main
* Utilise le nombre de cartes différentes, doublons, triplés, quadruplés dans la main

## Formule utilisée

* Pour calculer le nombre de combinaison possible, on utilise du dénombrement
    * Soit M une main
    * dif = nombre de cartes différentes de M
    * dou = nombre de doublons dans M
    * tri = nombre de triplés dans M
    * qua = le nombre de quadruplé dans M

    * Pour la chaque action, la formule correspondante est respectivement :
    * $$ Nmbccombi1= dif $$

    * $$ Nmbcombi2= doub + {dif \cdot (dif-1) \over 2} $$

    * $$ Nmbcombi3= tri + 2 \cdot doub \cdot (dif-1) + {doub \cdot (doub-1) \over 2} +3 { (dif-1) \cdot dif \cdot (2 \cdot dif-4) \over 12} $$

    * $$ Nmbcombi4=quad+2 \cdot trip \cdot (dif-1) +     3 {doub \cdot (doub-1) \over 2 } + 4  {doub \cdot  (dif-1) \cdot (dif-2) \over 2} + 6{ dif \cdot (dif-1) \cdot (dif^2 - 5 \cdot dif +6) \over 24} $$

### Explication des formules
* Dénombremment à faire plus tard