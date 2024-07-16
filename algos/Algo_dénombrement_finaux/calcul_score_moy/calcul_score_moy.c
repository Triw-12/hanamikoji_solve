#include "calcul_score.h"
#include "convertir.h"

int valeur_c[7] = {2, 2, 2, 3, 3, 4, 5};

bool verif_score_final(int *valide_moi, int *valide_adv)
{
    int cpt_moi = 0;
    int cpt_adv = 0;
    bool possible = true;
    for (int i = 0; i < 7; i++)
    {
        cpt_moi += valide_moi[i];
        cpt_adv += valide_adv[i];
        if (valide_moi[i] > valeur_c[i])
        {
            printf("TROP DE CARTES DE MEME VALEUR DE MON COTE POUR LA COULEUR %d : %d!\n", i, valide_moi[i]);
            possible = false;
        }
        if (valide_adv[i] > valeur_c[i])
        {
            printf("TROP DE CARTES DE MEME VALEUR DU COTE ADVERSE POUR LA COULEUR %d : %d!\n", i, valide_adv[i]);
            possible = false;
        }
    }
    if (cpt_moi != 8)
    {
        printf("LE COMPTE N'EST PAS BON DE MON COTE : %d \n", cpt_moi);
        possible = false;
    }
    if (cpt_adv != 8)
    {
        printf("LE COMPTE N'EST PAS BON DU COTE ADVERSE : %d \n", cpt_adv);
        possible = false;
    }
    return possible;
}

D_INT score(int *valide_moi, int *valide_adv, int *avantage)
{
    bool assertion = verif_score_final(valide_moi, valide_adv);
    if (!assertion)
    {
        printf("Moi %d %d %d %d %d %d %d\n", valide_moi[0], valide_moi[1], valide_moi[2], valide_moi[3], valide_moi[4], valide_moi[5], valide_moi[6]);
        printf("Adv %d %d %d %d %d %d %d\n", valide_adv[0], valide_adv[1], valide_adv[2], valide_adv[3], valide_adv[4], valide_adv[5], valide_adv[6]);
        fflush(stdout);
        assert(false);
    }
    D_INT res = {0, 0};
    for (int i = 0; i < 7; i++)
    {
        if (valide_moi[i] > valide_adv[i])
        {
            res.moi += valeur_c[i];
        }
        else if (valide_adv[i] > valide_moi[i])
        {
            res.adv += valeur_c[i];
        }
        else if (avantage[i] == 1)
        {
            res.moi += valeur_c[i];
        }
        else if (avantage[i] == -1)
        {
            res.adv += valeur_c[i];
        }
    }
    return res;
}

int diff_score(int *valide_moi, int *valide_adv, int *avantage)
{
    D_INT s = score(valide_moi, valide_adv, avantage);
    return s.moi - s.adv;
}

D_FLOAT *init_d_float(void)
{
    D_FLOAT *res = malloc(sizeof(D_FLOAT));
    res->pond = 0;
    res->som = 0;
    res->stats = NULL;
    return res;
}

float ponderation(void)
{
    return 1;
}

void ajout(D_FLOAT *simu, int *cartes_moi, int *cartes_adv, int *avantages, int n_m, int k_m, int *cartes_m, int *choix_m, int n_d, int k_d, int *cartes_d, int *choix_d)
{
    int sco = diff_score(cartes_moi, cartes_adv, avantages);
    float p = ponderation();
    simu->som += sco * p;
    simu->pond += p;
}

float total_simu(D_FLOAT *simu)
{
    float res = simu->som / simu->pond;
    free(simu);
    return res;
}

int main()
{
    /*
    //            TESTS
    int *cm = malloc(7 * sizeof(int));
    int *ca = malloc(7 * sizeof(int));
    int *av = malloc(7 * sizeof(int));
    int cm_i[7] = {2, 2, 2, 2, 0, 0, 0};
    int ca_i[7] = {0, 0, 0, 1, 1, 3, 3};
    int av_i[7] = {0, 0, 0, 0, 0, 0, 0};
    for (int i = 0; i < 7; i++)
    {
        cm[i] = cm_i[i];
        ca[i] = ca_i[i];
        av[i] = av_i[i];
    }
    printf("%d\n", cm, ca, av, cm, ca);
    D_FLOAT *r = init_d_float();
    ajout(r, cm, ca, av, cm, ca);
    printf("%f\n", total_simu(r));
    free(ca);
    free(cm);
    free(av);*/
    return 0;
}