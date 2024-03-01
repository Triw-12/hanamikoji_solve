#pragma once

#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>
#include <assert.h>

typedef struct double_int
{
    int moi; // Sommme
    int adv; // ponderation
} D_INT;

typedef struct double_float
{
    float som;
    float pond;
} D_FLOAT;

bool verif_score_final(int *valide_moi, int *valide_adv);

D_INT score(int *valide_moi, int *valide_adv, int *avantage);

int diff_score(int *valide_moi, int *valide_adv, int *avantage);

D_FLOAT *init_d_float(void);

float ponderation(void);

void ajout(D_FLOAT *simu, int sco);

float total_simu(D_FLOAT *simu);
