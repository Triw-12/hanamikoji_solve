#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <time.h>

int** nouv_manche(){
    //Renvois 2 paquets représentant les mains d'un joueur ainsi que les cartes qu'il piochera

    srand(time(NULL));

    int carte_t[22]={0,0,1,1,2,2,3,3,3,4,4,4,5,5,5,5,6,6,6,6,6,-1};
    int var_al;

    int** paquet=malloc(4*sizeof(int*));

    paquet[0]=malloc(6*sizeof(int));

    for (int j=0;j<6;j++){
        var_al=21;

        while (carte_t[var_al]==-1){
            var_al=rand()%21;
        } 

        paquet[0][j]=carte_t[var_al];
        carte_t[var_al]=-1;

    }

    paquet[1]=malloc(4*sizeof(int));

    for (int j=0;j<4;j++){
        var_al=21;

        while (carte_t[var_al]==-1){
            var_al=rand()%21;
        } 

        paquet[1][j]=carte_t[var_al];
        carte_t[var_al]=-1;
    }

    return paquet;
}