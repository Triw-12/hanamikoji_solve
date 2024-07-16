#pragma once

#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>
#include <assert.h>
#include "convertir.h"

typedef struct double_int
{
    int moi; // Sommme
    int adv; // ponderation
} D_INT;

typedef struct double_float
{
    float som;
    float pond;
    SIX ***stats;
} D_FLOAT;

bool verif_score_final(int *valide_moi, int *valide_adv);

D_INT score(int *valide_moi, int *valide_adv, int *avantage);

int diff_score(int *valide_moi, int *valide_adv, int *avantage);

D_FLOAT *init_d_float(SIX*** donnes);

void ajout(D_FLOAT *simu, int *cartes_moi, int *cartes_adv, int *avantages, int n_m, int k_m, int *cartes_m, int *choix_m, int n_d, int k_d, int *cartes_d, int *choix_d);

float total_simu(D_FLOAT *simu);
