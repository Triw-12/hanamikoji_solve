#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#define N_MAX 10

struct sixuplet
{
    int s;
    int d;
    int t;
    int q4;
    int q5;
    int prob;
};

typedef struct sixuplet SIX;

struct dictonnaire_lineraire
{
    int nb; // Le nb de cases
    int *k_p;
    SIX **dict;
};

typedef struct dictionnaire_lineraire DICO;

int lin(int n, int k, int s, int d, int t, int q4, int q5)
{
}

void creation(char *nom)
{
    FILE *fichier = fopen(nom, "r");
    int nb, nb_f;
    int nb_f_max = 0;
    int nb_lecture = 1;
    int init[7];
    int res[6];
    fscanf(fichier, "%d", &nb);
    printf("%d\n", nb);
    for (int i = 0; i < nb; i++)
    {
        for (int j = 0; j < 7; j++)
        {
            fscanf(fichier, "%d", &init[j]);
            nb_lecture++;
        }
        fscanf(fichier, "%d", &nb_f);
        nb_lecture++;
        // printf("i : %d nb_f : %d < %d  nb_lect : %d\n", i, nb_f, nb_f_max, nb_lecture);
        if (nb_f > nb_f_max)
        {
            nb_f_max = nb_f;
        }
        for (int j = 0; j < nb_f; j++)
        {
            for (int l = 0; l < 6; l++)
            {
                fscanf(fichier, "%d", &res[l]);
                nb_lecture++;
            }
        }
    }
    printf("%d\n", nb_f_max);
}

int main()
{
    creation("stats_cartes_doub.txt");
    // creation("stats_nb_doub.txt");
    return 0;
}