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

void affiche_l(int* lst,int n){
    //affiche la lst de taille n

    for (int i=0;i<n;i++){
        printf("%d\n",lst[i]);
    }
    printf("\n");
}

bool appart(int* lst, int deb, int fin, int elem){
    //Renvois si l'éléments est dans lst entre l'indice deb et fin

    for (int i=deb;i<fin;i++){
        if (lst[i]==elem){
            return true;
        }
    }

    return false;
}



int* tri_num(int n,int* lst){
    //Trie lst d'une manière précise (voir détail à part), lst de taille n
    
    int* lst_trie=malloc(n*sizeof(int));
    int* ind=malloc(5*sizeof(int));
    bool mis;
    int etape;
    int j;


    ind[0]=0;
    for (int i=1;i<5;i++){
        ind[i]=1;
    }

    lst_trie[0]=lst[0];
    for (int i=1;i<n;i++){  //On place chaque élément de lst
        mis=false;
        etape=0;

        while (etape<5 && appart(lst_trie,ind[etape],ind[etape+1],lst[i])){  //trouver l'étape correspondante
            etape++;
            
        }

 

        j=ind[4]-1;
                

        while (!mis){

             if ((j<ind[etape+1] && lst_trie[j]<lst[i]) || j<ind[etape]){

                lst_trie[j+1]=lst[i];
                mis=true;

            } else {

                lst_trie[j+1]=lst_trie[j];

                if (j==0){
                    lst_trie[0]=lst[i];
                    mis=true;
                } else {
                    j=j-1;
                }

            }

        }

        for (int i=etape+1;i<5;i++){
            ind[i]++;
        }
                
    }

    free(ind);

    lst=lst_trie;

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
    int* nmb_non=malloc(4*sizeof(int));    //entiers à enlever

    int c_nmb_non;  //nombre de fois qu'un entier a été enlevé
        
    if (action[0]){ //une carte est enlevée
        int nmb_sm1= nmb_fac_main[0];
        sous_manche[0]=malloc(nmb_sm1*sizeof(int*));

        for (int i=0; i<nmb_sm1; i++){
            sous_manche[0][i]=malloc((nmb_c-1)*sizeof(int));
            j=0;
            c_nmb_non=0;

            while (j<nmb_c){
                if (i==j){
                    j++;
                    c_nmb_non++;
                } else {
                    sous_manche[0][i][j-c_nmb_non]=hand[j];
                }
                j++;
            }

        }
    }

    if (action[1]){ //deux cartes enlevée
        int compt=0;

        int nmb_sm21=nmb_fac_main[1];   //nombre de sous manche en suprimant 2 cartes différentes
        int nmb_sm22=coefBinomial(2, nmb_fac_main[0]);   //nombre de sous manche en suprimant 2 cartes identiques
        int nmb_sm2= nmb_sm21+nmb_sm22; //nombre de sous manche en suprimant 2 cartes
        sous_manche[1]=malloc(nmb_sm2*sizeof(int*));

        for (int i=0; i<nmb_sm21; i++){
            sous_manche[1][i]=malloc((nmb_c-2)*sizeof(int));
            j=0;
            nmb_non[0]= hand[nmb_fac_main[0]+i];
            c_nmb_non=0;

            while (j<nmb_c){    //supprime 2 cartes identique
                if (c_nmb_non<2 && hand[j]==nmb_non[0]){
                    j++;
                    c_nmb_non++;
                } else {
                    sous_manche[1][i][j-c_nmb_non]=hand[j];
                }
            }
            
        }

        for (int i=0; i<nmb_fac_main[0]; i++){

            for (int l=i+1;l<nmb_fac_main[0];l++){
                sous_manche[1][compt+nmb_sm21]=malloc((nmb_c-2)*sizeof(int));
                j=0;

                while (j<nmb_c){
                    if (j==i || j==l){
                        j++;
                        c_nmb_non++;

                    } else {
                        sous_manche[1][compt+nmb_sm21][j-c_nmb_non]=hand[j];
                    }

                    j++;
                }

                compt++;
            }
            
        }

    }

    if (action[2]){

        int nmb_sm31=nmb_fac_main[2];
        int nmb_sm32=nmb_fac_main[1]*(nmb_fac_main[0]-1);
        int nmb_sm33=coefBinomial(nmb_fac_main[2], 2);

        int nmb_sm3=nmb_sm31+nmb_sm32+nmb_sm33;

        
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

    int* lst = malloc(7*sizeof(int));

    lst[0]=1;
    lst[1]=0;
    lst[2]=3;
    lst[3]=1;
    lst[4]=1;
    lst[5]=4;
    lst[6]=4;


    int* lst2=tri_num(7, lst);

    for (int i=0;i<7;i++){
        printf("%d \n",lst2[i]);
    }

    return 0;
}