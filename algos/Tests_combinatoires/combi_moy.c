#include <stdio.h>
#include <stdlib.h>


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

int nmb_combi(int* main,int cartes_t){

    int* nmb_c=combi_to_nmb(main,cartes_t);

    int nb_c1= nmb_c[0];

    int nb_c2= nmb_c[1]+    // 2 fois la même carte
    (nmb_c[0]*(nmb_c[0]-1))/2 ;  // 2 cates différentes

    int nb_c3= nmb_c[2]+    // 3 fois la même cartes
    2* nmb_c[1]*(nmb_c[0]-1)+    // 2 fois la même cartes et une autre carte
    3* (nmb_c[0]-1)*nmb_c[0]*(2*nmb_c[0]-4)/12 ; // 3 cartes différentes

    int nb_c4= nmb_c[3] +   // 4 fois la même cartes
    2* nmb_c[2]*(nmb_c[0]-1) +   // 3 fois la même cartes et 1 autre carte
    3* nmb_c[1]*(nmb_c[1]-1)/2 +   // 2 fois 2 cartes
    4* nmb_c[1]*( (nmb_c[0]-1) * (nmb_c[0]-2)/2) + // 2 fois deux cartes et 2 cartes différentes
    6* nmb_c[0]*(nmb_c[0]-1)* (nmb_c[0]*nmb_c[0]-5*nmb_c[0]+6)/24;    //4 cartes différentes           


    int nb_t=nb_c1+nb_c2+nb_c3+nb_c4;


    return nb_t;
}


int main(){

    int main[8]={0,0,0,1,2,2,3,5};

    int* tab=combi_to_nmb(main,8);

    printf ("1: %d\n2: %d\n3: %d\n4: %d\n",tab[0],tab[1],tab[2],tab[3]);



    return 0;
}