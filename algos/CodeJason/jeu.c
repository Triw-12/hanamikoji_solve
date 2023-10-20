#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <time.h>

int** nouv_manche(){
    //Renvois 4 paquets représentant les mains de chaques joueurs ainsi que les cartes qu'ils piocheront

    

    int** paquet=malloc(4*sizeof(int*));


    for (int i=0;i<4;i++){
        paquet[i]=malloc(4*sizeof(int));



    }
}