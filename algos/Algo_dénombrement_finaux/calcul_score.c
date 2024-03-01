#include "calcul_score.h"

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
    assert(verif_score_final(valide_moi, valide_adv));
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
    return res;
}

float ponderation(void)
{
    return 1;
}

void ajout(D_FLOAT *simu, int sco)
{
    float p = ponderation();
    simu->som += sco * p;
    simu->pond += p;
}

float total_simu(D_FLOAT *simu)
{
    return simu->som / simu->pond;
}