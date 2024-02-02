#include "api.h"
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

typedef struct cartes
{
    int *c;
} CARTES;

typedef struct etat
{
    int *valide_adv;
    int *valide_moi;
    int *avantage;

} ETAT;

typedef struct game
{
    int *cartes;
    int en_main;
    int defausse1;
    int defausse2;
    int valide;
    bool *act_poss;
    int *avantage;
} GAME;

typedef struct marqueurs
{
    int k;
    int n;
    int *cartes;
    int *pointeurs;
} marq;

GAME g;
int manche_accu = -1;
joueur moi;

void tri_cartes(int_array lc)
{
    for (int i = 0; i < 7; i++)
    {
        g.cartes[i] = 0;
    }
    for (int j = 0; j < lc.length; j++)
    {
        g.cartes[lc.items[j]] += 1;
        g.en_main += 1;
    }
}

void update(void)
{
    joueur poss;
    if (manche_accu != manche())
    {
        g.defausse1 = -1;
        g.defausse2 = -1;
        g.valide = -1;
        g.en_main = 0;
        for (int i = 0; i < 7; i++)
        {
            poss = possession_geisha(i);
            if (poss == moi)
            {
                g.avantage = 1;
            }
            else if (poss == EGALITE)
            {
                g.avantage = 0;
            }
            else
            {
                g.avantage = -1;
            }
        }
        for (int i = 0; i < 4; i++)
        {
            g.act_poss = true;
        }
        tri_cartes(cartes_en_main());
        manche_accu += 1;
    }
    else
    {
        action_jouee jouee = tour_precedent();
        int pioche = carte_pioche();
        g.cartes[pioche] += 1;
        g.en_main += 1;
    }
}

void joue_valide(int c)
{
    g.act_poss[0] = false;
    g.cartes[c] -= 1;
    g.en_main -= 1;
    g.valide = c;
    error e = action_valider(c);
    if (e == OK)
    {
        printf("Action valide carte : %d\n", c);
    }
    else
    {
        printf("ERREUR : %d\n", e);
    }
}

void joue_defausse(int d1, int d2)
{
    g.act_poss[1] = false;
    g.cartes[d1] -= 1;
    g.cartes[d2] -= 1;
    g.en_main -= 2;
    g.defausse1 = d1;
    g.defausse2 = d2;
    error e = action_defausser(d1, d2);
    if (e == OK)
    {
        printf("Action defausser cartes : %d, %d\n", d1, d2);
    }
    else
    {
        printf("ERREUR : %d\n", e);
    }
}

void joue_trois(int c1, int c2, int c3)
{
    g.act_poss[2] = false;
    g.cartes[c1] -= 1;
    g.cartes[c2] -= 1;
    g.cartes[c3] -= 1;
    g.en_main -= 4;
    error e = action_choix_trois(c1, c2, c3);
    if (e == OK)
    {
        printf("Action triple choix cartes : %d, %d %d\n", c1, c2, c3);
    }
    else
    {
        printf("ERREUR : %d\n", e);
    }
}

void joue_quatre(int c11, int c12, int c21, int c22)
{
    g.act_poss[3] = false;
    g.cartes[c11] -= 1;
    g.cartes[c12] -= 1;
    g.cartes[c21] -= 1;
    g.cartes[c22] -= 1;
    g.en_main -= 4;
    error e = action_choix_paquets(c11, c12, c21, c22);
    if (e == OK)
    {
        printf("Action choix paquets cartes : %d, %d %d %d\n", c11, c12, c21, c22);
    }
    else
    {
        printf("ERREUR : %d\n", e);
    }
}

marq *init_marqueur(int k, int n, int *cartes)
{
    marq *m = malloc(sizeof(marq));
    m->cartes = cartes;
    m->k = k;
    m->n = n;
    m->pointeurs = malloc(k * sizeof(int));
    int point = 0;
    int carte = 0;
    while (point < k && carte < 7)
    {
        for (int i = 0; i < cartes[carte] && point < k; i++)
        {
            m->pointeurs[point++] = carte;
        }
        carte++;
    }
    return m;
}

void choix_cartes(marq *m)
{
    int dernier_non_vide = m->k - 1;
    int non_plein = 6;
    int cpt;
    int continuer = true;
    while (dernier_non_vide >= 0 && continuer)
    {
        cpt = m->cartes[non_plein];
        while (cpt > 0 && continuer)
        {
            if (m->pointeurs[dernier_non_vide] == non_plein)
            {
                cpt--;
                dernier_non_vide--;
            }
            else
            {
                continuer = false;
            }
        }
        non_plein--;
    }
    m->pointeurs[dernier_non_vide++] = non_plein;
    for (int i = 0; i < cpt && dernier_non_vide < m->k; i++)
    {
        m->pointeurs[dernier_non_vide++] = non_plein;
    }
    non_plein++;
    while (dernier_non_vide < m->k && non_plein < 7)
    {
        for (int i = 0; i < m->cartes[non_plein] && dernier_non_vide < k; i++)
        {
            m->pointeurs[dernier_non_vide++] = non_plein;
        }
        non_plein++;
    }
}

// Fonction appelée au début du jeu
void init_jeu(void)
{
    printf("Début\n");
    g.cartes = malloc(7 * sizeof(int));
    g.avantage = malloc(7 * sizeof(int));
    g.act_poss = malloc(4 * sizeof(bool));
    moi = id_joueur();
}

// Fonction appelée au début du tour
void jouer_tour(void)
{
    update();
    for (int act = 0; act < 4; act++)
    {
        if (g.act_poss[act])
        {
            /// Pour chaque couple de cartes possibles
        }
    }
}

// Fonction appelée lors du choix entre les trois cartes lors de l'action de
// l'adversaire (cf tour_precedent)
void repondre_action_choix_trois(void)
{
}

// Fonction appelée lors du choix entre deux paquet lors de l'action de
// l'adversaire (cf tour_precedent)
void repondre_action_choix_paquets(void)
{
}

// Fonction appelée à la fin du jeu
void fin_jeu(void)
{
    free(g.cartes);
    free(g.avantage);
    printf("Fin\n");
}
