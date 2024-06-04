#pragma once

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <time.h>
#include <assert.h>
#define N_MAX 238

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

int lin(int k, int s, int d, int t, int q4, int q5);

int *delin(int i);

SIX ***creation(char *nom);

int proba(SIX ***tab, int n, int k, SIX debut, SIX arrive);

void free_six(SIX ***s);