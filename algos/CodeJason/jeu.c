#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <time.h>

int** nouv_manche(){
    //Renvois 4 paquets représentant les mains de chaques joueurs ainsi que les cartes qu'ils piocheront

    srand(time(NULL));

    int carte_t[22]={0,0,1,1,2,2,3,3,3,4,4,4,5,5,5,5,6,6,6,6,6,-1};
    int var_al;

    int** paquet=malloc(4*sizeof(int*));


    for (int i=0;i<4;i++){


        if (i%2==0){
            paquet[i]=malloc(6*sizeof(int));

            for (int j=0;j<6;j++){
            var_al=21;

            while (carte_t[var_al]==-1){
                var_al=rand()%21;
            } 

            paquet[i][j]=carte_t[var_al];
            carte_t[var_al]=-1;

            }

        } else {
            paquet[i]=malloc(4*sizeof(int));

            for (int j=0;j<4;j++){
            var_al=21;

            while (carte_t[var_al]==-1){
                var_al=rand()%21;
            } 

            paquet[i][j]=carte_t[var_al];
            carte_t[var_al]=-1;

            }   
        }
        
        
        

    }

    return paquet;
}