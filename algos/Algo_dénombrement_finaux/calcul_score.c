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

D_FLOAT *init_d_float(SIX*** donnes)
{
    D_FLOAT *res = malloc(sizeof(D_FLOAT));
    res->pond = 0;
    res->som = 0;
    res->stats = donnes;
    return res;
}

SIX doublons(int *cartes)
{
    SIX res = {.s = 0, .d = 0, .t = 0, .q4 = 0, .q5 = 0, .prob = 0};
    for (int i = 0; i < 7; i++)
    {
        switch (cartes[i])
        {
        case 1:
            res.s += 1;
            break;
        case 2:
            res.d += 1;
            break;
        case 3:
            res.t += 1;
            break;
        case 4:
            res.q4 += 1;
            break;
        case 5:
            res.q5 += 1;
            break;
        default:
            break;
        }
    }
    return res;
}

float ponderation(D_FLOAT *simu, int n_m, int k_m, int *cartes_m, int *choix_m, int n_d, int k_d, int *cartes_d, int *choix_d)
{
    printf("Debut pond\n");
    fflush(stdout);
    SIX doub_dep = doublons(cartes_m);
    SIX doub_fin = doublons(choix_m);
    int prob = proba(simu->stats, n_m, k_m, doub_dep, doub_fin);
    SIX doub_dep_d = doublons(cartes_d);
    SIX doub_fin_d = doublons(choix_d);
    int prob_d = proba(simu->stats, n_d, k_d, doub_dep_d, doub_fin_d);
    printf("Fin pond\n");
    fflush(stdout);
    return prob + prob_d;
}

void ajout(D_FLOAT *simu, int *cartes_moi, int *cartes_adv, int *avantages, int n_m, int k_m, int *cartes_m, int *choix_m, int n_d, int k_d, int *cartes_d, int *choix_d)
{
    int sco = diff_score(cartes_moi, cartes_adv, avantages);
    int* choix_m_bis = malloc(7*sizeof(int));
    int* choix_d_bis = malloc(7*sizeof(int));
    for (int i = 0; i < 7; i++){
        choix_m_bis[i] = 0;
        choix_d_bis[i] = 0;
    }
    for (int i = 0; i<k_m;i++){
        choix_m_bis[choix_m[i]] += 1;
    }
    for (int i = 0; i<k_d;i++){
        choix_d_bis[choix_d[i]] += 1;
    }
    float p = ponderation(simu, n_m, k_m, cartes_m, choix_m_bis, n_d, k_d, cartes_d, choix_d_bis);
    simu->som += sco * p;
    simu->pond += p;
}

float total_simu(D_FLOAT *simu)
{
    float res = simu->som / simu->pond;
    free(simu);
    return res;
}
