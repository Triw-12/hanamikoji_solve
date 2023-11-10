#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

#include "jeu.h"

int coefBinomial(int n, int k){
    //calcule k parmis n
 
    if (k > n)
        return 0;
    if (k == 0 || k == n)
        return 1;
  
    return coefBinomial(n-1, k-1) + coefBinomial(n-1, k);
}


int* combi_to_nmb(int* main,int cartes_t){
    //Renvois le nombre de carte différente, de doublons ( ou plus), de triplés (ou plus) et de quadruplé (ou plus) de la main

    int* nmb_c=malloc(4*sizeof(int));
    int nmb_g[7];

    for (int i=0;i<4;i++){
        nmb_c[i]=0;
    }

    for (int i=0;i<7;i++){  
        nmb_g[i]=0;
    }

    for (int i=0;i<cartes_t;i++){   //compte le nombre d'itération de chaque carte
        nmb_g[main[i]]++;
    }

    for (int i=0;i<7;i++){  //Pour chaque type de carte
        
        for (int j=1;j<5;j++){  //regarde si le nombre de carte dépasse j

            if (nmb_g[i]>=j){
                nmb_c[j-1]++;
            }

        }

    }

    return nmb_c;
}

int nmb_combi_tour(int* hand,int cartes_t,bool* action){
    //Renvois le nombre total de combinaison possible à partir de hand contenant cartes_t cartes et avec les actions possibles contenues dans action

    int* nmb_c=combi_to_nmb(hand,cartes_t);
    int nb_t=0;

    if (action[0]){
        int nb_c1= nmb_c[0];
        nb_t=nb_t+nb_c1;
    }
    
    if (action[1]){
       int nb_c2= nmb_c[1]+    // 2 fois la même carte
        (nmb_c[0]*(nmb_c[0]-1))/2 ;  // 2 cates différentes
        nb_t=nb_t+nb_c2;
    }

    if (action[2]){
        int nb_c3= nmb_c[2]+    // 3 fois la même cartes
        2* nmb_c[1]*(nmb_c[0]-1)+    // 2 fois la même cartes et une autre carte
        3* (nmb_c[0]-1)*nmb_c[0]*(2*nmb_c[0]-4)/12 ; // 3 cartes différentes
        nb_t=nb_t+nb_c3;
    }

    
    if (action[3]){
        int nb_c4= nmb_c[3] +   // 4 fois la même cartes
        2* nmb_c[2]*(nmb_c[0]-1) +   // 3 fois la même cartes et 1 autre carte
        3* nmb_c[1]*(nmb_c[1]-1)/2 +   // 2 fois 2 cartes
        4* nmb_c[1]*( (nmb_c[0]-1) * (nmb_c[0]-2)/2) + // 2 fois deux cartes et 2 cartes différentes
        6* nmb_c[0]*(nmb_c[0]-1)* (nmb_c[0]*nmb_c[0]-5*nmb_c[0]+6)/24;    //4 cartes différentes
        nb_t=nb_t+nb_c4;
    }

    return nb_t;
}

int*** main_sous_manche(int* hand, bool* action,int nmb_c){
    //Renvois toute les sous manches possible à la suite d'une manche dont la main est hand et avec actio la liste des actions possibles, trie les sous manches en fonctions de l'action réalisée
    int*** sous_manche=malloc(4*sizeof(int**));

    int* nmb_fac_main=combi_to_nmb(hand,nmb_c);
    
    int j;
        
    if (action[0]){ //une carte est enlevée
        int nmb_sm1= nmb_fac_main[0];
        sous_manche[0]=malloc(nmb_sm1*sizeof(int*));

        for (int i=0; i<nmb_sm1; i++){
            sous_manche[0][i]=malloc((nmb_c-1)*sizeof(int));
            j=0;

            while (j<nmb_c-1){
                if (i=j){
                    j++;
                } else {
                    sous_manche[0][i][j]=hand[j];
                }
                j++;
            }

        }
    }

    if (action[1]){ //deux cartes enlevée
        int nmb_sm2=nmb_fac_main[1]+coefBinomial(2, nmb_fac_main[0]);
        sous_manche[1]=malloc(nmb_sm2*sizeof(int*));

        for (int i=0; i<nmb_sm2; i++){
            sous_manche[1][i]=malloc((nmb_c-1)*sizeof(int));
        }



    }



    if (action[1]){

        sous_manche[1]=malloc(sizeof(int));
    }



}

int nmb_combi_manche(int** manche, int* hand, int nmb_c){
    //renvois le nombre total de combinaison dans une manche prédéfini



    for (int i=0;i<6;i++){
        hand[i]=manche[0][i];
    }

    for (int i=0;i<4;i++){
        hand[nmb_c]=manche[1][i];
        nmb_c++;




    }


}



int main(){



    return 0;
}