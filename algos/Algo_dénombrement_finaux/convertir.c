#include "convertir.h"

int lin(int k, int s, int d, int t, int q4, int q5)
{
    return 1920 * (k - 1) + 240 * s + 30 * d + 6 * t + 2 * q4 + q5;
}

int *delin(int i)
{
    int *res = malloc(6 * sizeof(int));
    res[5] = i % 2;
    i = i / 2;
    res[4] = i % 3;
    i = i / 3;
    res[3] = i % 5;
    i = i / 5;
    res[2] = i % 8;
    i = i / 8;
    res[1] = i % 8;
    i = i / 8;
    res[0] = i;
    return res;
}

SIX ***creation(char *nom)
{
    printf("Recuperation des donnes\n");
    fflush(stdout);
    int j;
    SIX ***res_s = malloc(20 * sizeof(SIX **));
    assert(res_s != NULL);
    SIX base = {.s = -1, .d = -1, .t = -1, .q4 = -1, .q5 = -1, .prob = -1};
    for (int i = 0; i < 20; i++)
    {
        j = (1920 * (i + 1) + 240 * 8 + 30 * 8 + 6 * 5 + 2 * 3 + 2);
        res_s[i] = malloc(j * sizeof(SIX *));
        assert(res_s[i] != NULL);
        for (int k = 0; k < j; k++)
        {
            res_s[i][k] = malloc(N_MAX * sizeof(SIX));
            assert(res_s[i][k] != NULL);
            for (int l = 0; l < N_MAX; l++)
            {
                res_s[i][k][l] = base;
            }
        }
    }
    printf("Fin de creation\n");
    fflush(stdout);
    SIX en_place;
    FILE *fichier = fopen(nom, "r");
    int nb, nb_f, cpt, ind;
    int nb_f_max = 0;
    int nb_lecture = 1;
    int init[7];
    int res[6];
    fscanf(fichier, "%d", &nb);
    printf("%d\n", nb);
    for (int i = 0; i < nb; i++)
    {
        //printf("%d\n",i);
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
        ind = lin(init[1], init[2], init[3], init[4], init[5], init[6]);
        //printf("Init : %d %d %d %d %d %d %d\n", init[0], init[1], init[2], init[3], init[4], init[5], init[6]);
        //printf("Ind : %d\n", ind);
        cpt = 0;
        for (int j = 0; j < nb_f; j++)
        {
            for (int l = 0; l < 6; l++)
            {
                fscanf(fichier, "%d", &res[l]);
                nb_lecture++;
            }
            en_place.s = res[0];
            en_place.d = res[1];
            en_place.t = res[2];
            en_place.q4 = res[3];
            en_place.q5 = res[4];
            en_place.prob = res[5];
            //printf("Res : %d %d %d %d %d %d %d\n", res[0], res[1], res[2], res[3], res[4], res[5], cpt);
            res_s[init[0] - 1][ind][cpt++] = en_place;
            //printf("OK\n");
        }
    }
    // printf("%d\n", nb_f_max);
    printf("Fin des recuperation des donnes\n");
    fflush(stdout);
    return res_s;
}

int proba(SIX ***tab, int n, int k, SIX debut, SIX arrive)
{
    int ind = lin(k, debut.s, debut.d, debut.t, debut.q4, debut.q5);
    printf("Debut proba %d %d %d %d %d %d %d %d\n",n,k, debut.s, debut.d, debut.t, debut.q4, debut.q5,ind);
    printf("Arrive : %d %d %d %d %d\n",arrive.s, arrive.d, arrive.t, arrive.q4, arrive.q5);
    fflush(stdout);
    SIX val;
    for (int i = 0; i < N_MAX; i++)
    {
        printf("OK %d\n",i);
        fflush(stdout);
        val = tab[n][ind][i];
        printf("VAL : %d %d %d %d %d\n",val.s, val.d, val.t, val.q4, val.q5);
        fflush(stdout);
        assert(val.s != -1);
        if (val.s == arrive.s && val.d == arrive.d && val.t == arrive.t && val.q4 == arrive.q4 && val.q5 == arrive.q5)
        {
            printf("Val_prob = %d",val.prob);
            fflush(stdout);
            return val.prob;
        }
    }
    assert(false);
    return 0;
}

void free_six(SIX ***s)
{
    int j;
    for (int i = 0; i < 20; i++)
    {
        j = (1920 * (i + 1) + 240 * 8 + 30 * 8 + 6 * 5 + 2 * 3 + 2);
        for (int k = 0; k < j; k++)
        {
            free(s[i][k]);
        }
        free(s[i]);
    }
    free(s);
}

/*
int main()
{
    int t1 = time(NULL);
    creation("stats_cartes_doub.txt");
    // creation("stats_nb_doub.txt");
    int t2 = time(NULL);
    printf("Temps : %d\n", t2 - t1);
    return 0;
}
*/