#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

typedef struct marqueurs
{
    int k;
    int n;
    int *cartes;
    int *pointeurs;
} marq;

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
        while (cpt > 0 && dernier_non_vide >= 0 && continuer)
        {
            // printf("e: %d %d %d\n", m->pointeurs[dernier_non_vide], non_plein, cpt);
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
    // printf("Non final : %d\n", dernier_non_vide);
    if (dernier_non_vide < 0)
    {
        free(m->pointeurs);
        m->pointeurs = NULL;
    }
    else
    {
        non_plein = m->pointeurs[dernier_non_vide] + 1;
        while (m->cartes[non_plein] == 0)
        {
            non_plein++;
        }
        m->pointeurs[dernier_non_vide] = non_plein;
        cpt = m->cartes[m->pointeurs[dernier_non_vide]] - 1;
        dernier_non_vide++;
        // printf("e : %d %d %d\n", dernier_non_vide, non_plein, cpt);
        for (int i = 0; i < cpt && dernier_non_vide < m->k; i++)
        {
            // printf("Fait\n");
            m->pointeurs[dernier_non_vide++] = non_plein;
        }
        non_plein++;
        // printf("%d %d\n", dernier_non_vide, non_plein);
        while (dernier_non_vide < m->k && non_plein < 7)
        {
            // printf("%d %d\n", dernier_non_vide, non_plein);
            for (int i = 0; i < m->cartes[non_plein] && dernier_non_vide < m->k; i++)
            {
                m->pointeurs[dernier_non_vide++] = non_plein;
            }
            non_plein++;
        }
        if (dernier_non_vide < m->k && non_plein >= 7)
        {
            free(m->pointeurs);
            m->pointeurs = NULL;
        }
    }
}

int main()
{
    int *cartes = malloc(7 * sizeof(int));
    cartes[0] = 3;
    cartes[1] = 1;
    cartes[2] = 0;
    cartes[3] = 0;
    cartes[4] = 0;
    cartes[5] = 2;
    cartes[6] = 1;
    marq *m = init_marqueur(4, 7, cartes);
    while (m->pointeurs != NULL)
    {
        for (int p = 0; p < m->k; p++)
        {
            printf("%d ", m->pointeurs[p]);
        }
        printf("\n");
        choix_cartes(m);
    }
    return 0;
}
