#include "api.h"
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include "calcul_score.h"
#include <sys/time.h>

typedef struct etat
{
    int *valide_adv; // Les cartes déjà validés par mon adversaire
    int *valide_moi; // Les caryes déjà validés par moi
    int *avantage;   // -1 si l'avantage est à mon adversaire +1 si c'est moi 0 sinon (en fonction de chaque couleur)
} ETAT;

typedef struct game
{
    int *cartes;
    int *restantes;
    int en_main;
    int nb_restantes;
    int valide;
    int defausse1;
    int defausee2;
    bool *act_poss;
    ETAT *etat;
} GAME; // L'état actuel du jeu

typedef struct marqueurs
{
    int k;          // la taille de pointeurs // le nombre de cartes choisis
    int n;          // le nombre de cartes dans lequel on choisit
    int *cartes;    // Les cartes dans lequel on choisit
    int *pointeurs; // Les cartes choisis
} marq;

typedef struct coup
{
    int action;
    int *cartes;
} COUP;

GAME g;
int manche_accu = -1;
joueur moi;
joueur adv;

// LES CONSTANTES
int valeur_couleur[7] = {2, 2, 2, 3, 3, 4, 5};                     // La valeur des couleurs = au nombre de cartes
int permu_trois[3][2] = {{1, 2}, {0, 2}, {0, 1}};                  // Les deux cartes non choisis
int permu_paquet[2][4] = {{0, 1, 2, 3}, {2, 3, 0, 1}};             // Les permutations pour deux paquets
int nb_cartes_par_action[4][2] = {{1, 0}, {0, 0}, {2, 1}, {2, 2}}; // Le nombre de cartes validés par action en fonction des joueurs

long t1;
long currenttime()
{
    /*Renvoie le temps actuel en millisecondes*/
    struct timeval tp;
    gettimeofday(&tp, NULL);
    return tp.tv_sec * 1000 + tp.tv_usec / 1000;
}

void debug_cartes(int nb, int *ens_cartes, char *nom)
{
    /*Affiche le paquet de carte ens_cartes comprendant nb cases en affichant nom avant*/
    printf("%s : ", nom);
    for (int i = 0; i < nb; i++)
    {
        printf("%d ", ens_cartes[i]);
    }
    printf("\n");
    fflush(stdout);
}

void toutes_les_cartes(int *ens_cartes)
{
    /*Initialise le tableau ens_cartes aux valeurs contenues dans valeur_couleur (variable globale)*/
    for (int i = 0; i < 7; i++)
    {
        ens_cartes[i] = valeur_couleur[i];
    }
}

void aucune_carte(int *ens_cartes)
{
    /*Initialise le tableau ens_cartes à 0*/
    for (int i = 0; i < 7; i++)
    {
        ens_cartes[i] = 0;
    }
}

void update_cartes_valides(void)
{
    /*Met à jour les cartes validées et restantes*/
    toutes_les_cartes(g.restantes);
    g.nb_restantes = 0;
    for (int i = 0; i < 7; i++)
    {
        g.etat->valide_moi[i] = nb_cartes_validees(moi, i);
        g.etat->valide_adv[i] = nb_cartes_validees(adv, i);
        g.restantes[i] = g.restantes[i] - g.etat->valide_moi[i] - g.etat->valide_adv[i] - g.cartes[i];
        g.nb_restantes += g.restantes[i];
    }
    if (!(g.act_poss[0])) // Carte validée secretement
    {
        g.restantes[g.valide] -= 1;
        g.etat->valide_moi[g.valide] += 1;
    }
    if (!(g.act_poss[1])) // Cartes defaussés
    {
        g.restantes[g.defausse1] -= 1;
        g.restantes[g.defausee2] -= 1;
        g.nb_restantes -= 2;
    }
}

void update(bool new_c)
{
    /*Met à jour l'état du jeu au début d'un tour*/
    joueur poss;
    if (manche_accu != manche()) // Pour une nouvelle manche
    {
        g.valide = -1;
        g.en_main = 0;
        g.defausse1 = -1;
        g.defausee2 = -1;
        for (int i = 0; i < 7; i++) // On regarde les avantages de chaque couleur
        {
            poss = possession_geisha(i);
            if (poss == moi)
            {
                g.etat->avantage[i] = 1;
            }
            else if (poss == EGALITE)
            {
                g.etat->avantage[i] = 0;
            }
            else
            {
                g.etat->avantage[i] = -1;
            }
        }
        for (int i = 0; i < 4; i++) // Toutes les actions sont à nouveau disponible
        {
            g.act_poss[i] = true;
        }
        int_array lc = cartes_en_main();
        aucune_carte(g.cartes);
        for (int j = 0; j < lc.length; j++) // Mets à jour les cartes en main
        {
            g.cartes[lc.items[j]] += 1;
            g.en_main += 1;
        }
        update_cartes_valides();
        manche_accu += 1;
    }
    else
    {
        if (new_c) // Si c'est juste un nouveau tour, ajoute la carte piochée (si elle existe (en fonction de new_c))
        {
            int pioche = carte_piochee();
            g.cartes[pioche] += 1;
            g.en_main += 1;
        }
        update_cartes_valides();
    }
}

void joue_valide(int c)
{
    /*Joue l'action valider avec la carte c*/
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
        printf("!!!!!!!!!!!!!!!!!!! ERREUR !!!!!!!!!!!: %d\n", e);
        printf("Action valide carte : %d\n", c);
    }
}

void joue_defausse(int d1, int d2)
{
    /*Joue l'action défausser avec les cartes d1 et d2*/
    g.act_poss[1] = false;
    g.cartes[d1] -= 1;
    g.cartes[d2] -= 1;
    g.en_main -= 2;
    g.defausse1 = d1;
    g.defausee2 = d2;
    error e = action_defausser(d1, d2);
    if (e == OK)
    {
        printf("Action defausser cartes : %d, %d\n", d1, d2);
    }
    else
    {
        printf("!!!!!!!!!!!!!!!!!!! ERREUR !!!!!!!!!!!: %d\n", e);
        printf("Action defausser cartes : %d, %d\n", d1, d2);
    }
}

void joue_trois(int c1, int c2, int c3)
{
    /*Joue l'action 3 avec les cartes c1, c2 et c3*/
    g.act_poss[2] = false;
    g.cartes[c1] -= 1;
    g.cartes[c2] -= 1;
    g.cartes[c3] -= 1;
    g.en_main -= 4;
    error e = action_choix_trois(c1, c2, c3);
    if (e == OK)
    {
        printf("Action triple choix cartes : %d, %d, %d\n", c1, c2, c3);
    }
    else
    {
        printf("!!!!!!!!!!!!!!!!!!! ERREUR !!!!!!!!!!!: %d\n", e);
        printf("Action triple choix cartes : %d, %d, %d\n", c1, c2, c3);
    }
}

void joue_quatre(int c11, int c12, int c21, int c22)
{
    /*Joue l'action des paquets avec les cartes c11 et c12 d'un coté, et les cartes c21 et c22 de l'autre*/
    g.act_poss[3] = false;
    g.cartes[c11] -= 1;
    g.cartes[c12] -= 1;
    g.cartes[c21] -= 1;
    g.cartes[c22] -= 1;
    g.en_main -= 4;
    error e = action_choix_paquets(c11, c12, c21, c22);
    if (e == OK)
    {
        printf("Action choix paquets cartes : %d %d %d %d\n", c11, c12, c21, c22);
    }
    else
    {
        printf("!!!!!!!!!!!!!!!!!!! ERREUR !!!!!!!!!!!: %d\n", e);
        printf("Action choix paquets cartes : %d, %d, %d, %d\n", c11, c12, c21, c22);
    }
}

marq *init_marqueur(int k, int n, int *cartes)
{
    /*Initialise le marqueur pour choisir k cartes parmis les n cartes dans cartes*/
    assert(k < n);
    marq *m = malloc(sizeof(marq));
    m->cartes = cartes;
    m->k = k;
    m->n = n;
    m->pointeurs = malloc(k * sizeof(int));
    int point = 0;
    int carte = 0;
    while (point < k && carte < 7)
    {
        // prend la première carte possible
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
    /*Le marqueur m propose un nouveau choix de cartes dans la case pointeur, et NULL s'il en existe plus*/
    int dernier_non_vide = m->k - 1;
    int non_plein = 6;
    int cpt;
    int continuer = true;
    // cherche la première case vide pour faire avancer un pointeur
    while (dernier_non_vide >= 0 && continuer)
    {
        cpt = m->cartes[non_plein];
        while (cpt > 0 && dernier_non_vide >= 0 && continuer)
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

    if (dernier_non_vide < 0) // il n'y a plus de cases vides
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
        for (int i = 0; i < cpt && dernier_non_vide < m->k; i++)
        { // On repositionne les pointeurs suivants
            m->pointeurs[dernier_non_vide++] = non_plein;
        }
        non_plein++;
        while (dernier_non_vide < m->k && non_plein < 7)
        { // On décale tous les autres pointeurs
            for (int i = 0; i < m->cartes[non_plein] && dernier_non_vide < m->k; i++)
            {
                m->pointeurs[dernier_non_vide++] = non_plein;
            }
            non_plein++;
        }
        if (dernier_non_vide < m->k && non_plein >= 7) // Si les derniers pointeurs n'ont plus la place
        {
            free(m->pointeurs);
            m->pointeurs = NULL;
        }
    }
}

void free_marq(marq *m)
{
    /*Déalloue la mémoire du marqueur m*/
    if (m->pointeurs != NULL)
    {
        free(m->pointeurs);
    }
    free(m);
}

bool verification(int nb_cartes, int *cartes, int nb_restantes, int *restantes, int nb_selec, int *select, ETAT *etat, bool *act_poss_simu)
{
    /*Vérifie si la distribution des cartes est possible
    Entree : cartes : les cartes en main
             restantes : les cartes que l'on a toujours pas vu
             select : les cartes que l'on voudrait valider de notre coté
             etat : l'état du jeu
             act_poss_simu : les actions encore possible (après simulation)*/
    int nb_moi_max = 0;
    int nb_moi_min = 0;
    for (int i = 0; i < 4; i++)
    {
        if (act_poss_simu[i])
        {
            nb_moi_max += nb_cartes_par_action[i][0];
        }
    }
    int tour_a = tour();
    int t; // Le nombre de cartes que l'on a pas encore vu et qui vont arriver dans notre main
    if (moi == 1 && tour_a == 0)
    {
        t = 4;
    }
    else if (tour_a == 0 || tour_a == 1 || (tour_a == 2 && moi == 1))
    {
        t = 3;
    }
    else if (tour_a == 2 || tour_a == 3 || (tour_a == 4 && moi == 1))
    {
        t = 2;
    }
    else if (tour_a == 4 || tour_a == 5 || (tour_a == 6 && moi == 1))
    {
        t = 1;
    }
    else
    {
        t = 0;
    }
    if (nb_moi_max - t > 0)
    {
        nb_moi_min = nb_moi_max - t;
    }
    int nb_moi_borne_inf = 0;
    int nb_moi_borne_sup = 0;
    int restantes_d[7];
    int cartes_d[7];
    for (int c = 0; c < 7; c++)
    {
        restantes_d[c] = restantes[c];
        cartes_d[c] = cartes[c];
    }
    for (int c = 0; c < nb_selec; c++)
    {
        restantes_d[select[c]] -= 1;
        cartes_d[select[c]] -= 1;
    }
    for (int c = 0; c < 7; c++)
    {
        nb_moi_borne_sup += cartes[c] - cartes_d[c]; // On prend en priorité les cartes qui sont dans notre main
        if (restantes_d[c] < 0)
        {
            nb_moi_borne_inf -= restantes_d[c]; // On prend en priorié les cartes qui ne sont pas dans notre main
        }
    }
    if (nb_moi_borne_inf > nb_moi_max || nb_moi_borne_sup < nb_moi_min)
    {
        // printf("Coup impossible %d %d %d %d\n", nb_moi_borne_inf, nb_moi_max, nb_moi_borne_sup, nb_moi_min);
        return false;
    }
    else
    {
        return true;
    }
}

float simulation_coup(int nb_cartes, int *cartes, int nb_restantes, int *restantes, bool action_defausse, ETAT *etat, bool *act_poss_simu)
{
    /*Simule un coup et renvoie son score pour le coup simulé joué*/
    // INITIALISATION
    D_FLOAT *res = init_d_float();
    int nb_mon_cote = 8;
    int nb_cote_adv = 8;
    int nb_total = nb_cartes + nb_restantes;
    int *total = malloc(7 * sizeof(int));
    int *total_s_moi = malloc(7 * sizeof(int));
    int *cartes_adv = malloc(7 * sizeof(int));
    int *cartes_moi = malloc(7 * sizeof(int));
    for (int i = 0; i < 7; i++)
    {
        nb_mon_cote -= etat->valide_moi[i];
        nb_cote_adv -= etat->valide_adv[i];
        total[i] = cartes[i] + restantes[i];
        total_s_moi[i] = cartes[i] + restantes[i];
        cartes_adv[i] = etat->valide_adv[i] + cartes[i] + restantes[i];
        cartes_moi[i] = etat->valide_moi[i];
    }
    marq *mon_cote = init_marqueur(nb_mon_cote, nb_total, total);
    marq *defausse;

    // Distribution des cartes
    while (mon_cote->pointeurs != NULL)
    {
        if (verification(nb_cartes, cartes, nb_restantes, restantes, nb_mon_cote, mon_cote->pointeurs, etat, act_poss_simu))
        {
            for (int i = 0; i < mon_cote->k; i++)
            {
                total_s_moi[mon_cote->pointeurs[i]] -= 1;
                cartes_adv[mon_cote->pointeurs[i]] -= 1;
                cartes_moi[mon_cote->pointeurs[i]] += 1;
            }
            if (!action_defausse)
            {
                defausse = init_marqueur(3, nb_total - mon_cote->k, total_s_moi);
            }
            else
            {
                defausse = init_marqueur(5, nb_total - mon_cote->k, total_s_moi);
            }
            while (defausse->pointeurs != NULL)
            {
                for (int i = 0; i < defausse->k; i++)
                {
                    cartes_adv[defausse->pointeurs[i]] -= 1;
                }
                ajout(res, diff_score(cartes_moi, cartes_adv, g.etat->avantage)); // On calcule le score de cette fin de partie
                for (int i = 0; i < defausse->k; i++)
                {
                    cartes_adv[defausse->pointeurs[i]] += 1;
                }
                choix_cartes(defausse);
            }

            // On remet à l'état initial
            free_marq(defausse);
            for (int i = 0; i < mon_cote->k; i++)
            {
                total_s_moi[mon_cote->pointeurs[i]] += 1;
                cartes_adv[mon_cote->pointeurs[i]] += 1;
                cartes_moi[mon_cote->pointeurs[i]] -= 1;
            }
        }
        choix_cartes(mon_cote);
    }

    // Libération de mémoire
    free_marq(mon_cote);
    free(total);
    free(total_s_moi);
    free(cartes_adv);
    free(cartes_moi);
    return total_simu(res);
}

// Fonction appelée au début du jeu
void init_jeu(void)
{
    // ALLOCATION DE MEMOIRE
    t1 = currenttime();
    printf("Debut match\n");
    g.cartes = malloc(7 * sizeof(int));
    g.etat = malloc(sizeof(ETAT));
    g.etat->valide_adv = malloc(7 * sizeof(int));
    g.etat->valide_moi = malloc(7 * sizeof(int));
    g.etat->avantage = malloc(7 * sizeof(int));
    g.act_poss = malloc(4 * sizeof(bool));
    g.restantes = malloc(7 * sizeof(int));
    moi = id_joueur();
    if (moi == 0)
    {
        adv = 1;
    }
    else
    {
        adv = 0;
    }
    printf("Fin de l'initialisation du tour : %ld\n\n", currenttime() - t1);
}

// Fonction appelée au début du tour
void jouer_tour(void)
{
    // INITIALISATION TOUR
    printf("Debut : manche %d  tour %d\n", manche(), tour());
    t1 = currenttime();
    update(true);
    printf("Update termine : defausser %d\n", g.act_poss[1]);
    debug_cartes(7, g.cartes, "Mes cartes");
    debug_cartes(7, g.restantes, "Cartes restantes");
    float score_maxi = -50;
    COUP coup_maxi;
    coup_maxi.cartes = malloc(4 * sizeof(int));
    coup_maxi.cartes[0] = -1;
    coup_maxi.cartes[1] = -1;
    coup_maxi.cartes[2] = -1;
    coup_maxi.cartes[3] = -1;
    float res;

    marq *tour_simu;
    int *cartes_simu = malloc(7 * sizeof(int));
    ETAT *etat_simu = malloc(sizeof(ETAT));
    etat_simu->avantage = malloc(7 * sizeof(int));
    etat_simu->valide_adv = malloc(7 * sizeof(int));
    etat_simu->valide_moi = malloc(7 * sizeof(int));
    bool *act_poss_simu = malloc(4 * sizeof(int));
    for (int i = 0; i < 4; i++)
    {
        act_poss_simu[i] = g.act_poss[i];
    }
    for (int c = 0; c < 7; c++)
    {
        cartes_simu[c] = g.cartes[c];
        etat_simu->avantage[c] = g.etat->avantage[c];
        etat_simu->valide_adv[c] = g.etat->valide_adv[c];
        etat_simu->valide_moi[c] = g.etat->valide_moi[c];
    }
    printf("Fin de copie de l'etat du jeu : %ld\n", currenttime() - t1);

    ///// VALIDER UNE CARTE
    if (g.act_poss[0])
    {
        act_poss_simu[0] = false;
        tour_simu = init_marqueur(1, g.en_main, g.cartes);
        while (tour_simu->pointeurs != NULL)
        {
            cartes_simu[tour_simu->pointeurs[0]] -= 1;
            etat_simu->valide_moi[tour_simu->pointeurs[0]] += 1;
            res = simulation_coup(tour_simu->n - tour_simu->k, cartes_simu, g.nb_restantes, g.restantes, g.act_poss[1], etat_simu, act_poss_simu);
            if (res > score_maxi) // On regarde quel coup à un score maximal
            {
                score_maxi = res;
                coup_maxi.action = 1;
                coup_maxi.cartes[0] = tour_simu->pointeurs[0];
            }
            ////// APRES LA SIMULATION
            cartes_simu[tour_simu->pointeurs[0]] += 1;
            etat_simu->valide_moi[tour_simu->pointeurs[0]] -= 1;
            choix_cartes(tour_simu);
        }
        free_marq(tour_simu);
        act_poss_simu[0] = true;
    }
    printf("Fin simu valider\n");

    // DEFAUSSER UNE CARTE
    if (g.act_poss[1])
    {
        act_poss_simu[1] = false;
        tour_simu = init_marqueur(2, g.en_main, g.cartes);
        while (tour_simu->pointeurs != NULL)
        {
            cartes_simu[tour_simu->pointeurs[0]] -= 1;
            cartes_simu[tour_simu->pointeurs[1]] -= 1;
            res = simulation_coup(tour_simu->n - tour_simu->k, cartes_simu, g.nb_restantes, g.restantes, false, etat_simu, act_poss_simu);
            if (res > score_maxi)
            {
                score_maxi = res;
                coup_maxi.action = 2;
                coup_maxi.cartes[0] = tour_simu->pointeurs[0];
                coup_maxi.cartes[1] = tour_simu->pointeurs[1];
            }
            ////// APRES LA SIMULATION
            cartes_simu[tour_simu->pointeurs[0]] += 1;
            cartes_simu[tour_simu->pointeurs[1]] += 1;
            choix_cartes(tour_simu);
        }
        free_marq(tour_simu);
        act_poss_simu[1] = true;
    }
    printf("Fin simu defausser\n");

    float score_mini;
    COUP coup_mini;
    coup_mini.cartes = malloc(4 * sizeof(int));
    coup_mini.cartes[0] = -1;
    coup_mini.cartes[1] = -1;
    coup_mini.cartes[2] = -1;
    coup_mini.cartes[3] = -1;
    if (g.act_poss[2])
    {
        act_poss_simu[2] = false;
        score_mini = 50;
        coup_mini.action = 3;
        tour_simu = init_marqueur(3, g.en_main, g.cartes);
        while (tour_simu->pointeurs != NULL)
        {
            cartes_simu[tour_simu->pointeurs[0]] -= 1;
            cartes_simu[tour_simu->pointeurs[1]] -= 1;
            cartes_simu[tour_simu->pointeurs[2]] -= 1;
            for (int c = 0; c < 3; c++)
            {
                /*On regarde le score en fonction de la carte qu'il va prendre*/
                etat_simu->valide_adv[tour_simu->pointeurs[c]] += 1;
                etat_simu->valide_moi[tour_simu->pointeurs[permu_trois[c][0]]] += 1;
                etat_simu->valide_moi[tour_simu->pointeurs[permu_trois[c][1]]] += 1;

                res = simulation_coup(tour_simu->n - tour_simu->k, cartes_simu, g.nb_restantes, g.restantes, g.act_poss[1], etat_simu, act_poss_simu);
                if (res < score_mini)
                { // On choisit le score minimisant les coups qu'il fait
                    score_mini = res;
                    coup_mini.cartes[0] = tour_simu->pointeurs[0];
                    coup_mini.cartes[1] = tour_simu->pointeurs[1];
                    coup_mini.cartes[2] = tour_simu->pointeurs[2];
                }
                etat_simu->valide_adv[tour_simu->pointeurs[c]] -= 1;
                etat_simu->valide_moi[tour_simu->pointeurs[permu_trois[c][0]]] -= 1;
                etat_simu->valide_moi[tour_simu->pointeurs[permu_trois[c][1]]] -= 1;
            }

            if (score_mini != 50 && score_mini > score_maxi)
            { // On choisit le coup qui maximise les 'pires choix possibles'
                score_maxi = score_mini;
                coup_maxi.action = coup_mini.action;
                coup_maxi.cartes[0] = coup_mini.cartes[0];
                coup_maxi.cartes[1] = coup_mini.cartes[1];
                coup_maxi.cartes[2] = coup_mini.cartes[2];
            }
            ////// On revient à l'état initial
            cartes_simu[tour_simu->pointeurs[0]] += 1;
            cartes_simu[tour_simu->pointeurs[1]] += 1;
            cartes_simu[tour_simu->pointeurs[2]] += 1;
            choix_cartes(tour_simu);
        }
        free_marq(tour_simu);
        act_poss_simu[2] = true;
    }
    printf("Fin simu choix 3\n");

    // CHOIX DES PAQUETS
    int cpt, cpt_adv, place;
    if (g.act_poss[3])
    {
        act_poss_simu[3] = false;
        coup_mini.action = 4;
        int *cartes_choisis = malloc(7 * sizeof(int));
        int *ordre = malloc(4 * sizeof(int));
        tour_simu = init_marqueur(4, g.en_main, g.cartes);
        aucune_carte(cartes_choisis);
        while (tour_simu->pointeurs != NULL)
        {
            cartes_simu[tour_simu->pointeurs[0]] -= 1;
            cartes_simu[tour_simu->pointeurs[1]] -= 1;
            cartes_simu[tour_simu->pointeurs[2]] -= 1;
            cartes_simu[tour_simu->pointeurs[3]] -= 1;
            cartes_choisis[tour_simu->pointeurs[0]] += 1;
            cartes_choisis[tour_simu->pointeurs[1]] += 1;
            cartes_choisis[tour_simu->pointeurs[2]] += 1;
            cartes_choisis[tour_simu->pointeurs[3]] += 1;
            marq *prem_paquet = init_marqueur(2, 4, cartes_choisis);
            while (prem_paquet->pointeurs != NULL)
            {
                // Pour chaque possiblité d'associer les cartes 2 par 2
                cpt = 0;
                cpt_adv = 2;
                score_mini = 50;
                // POSSIBILITE 1 : il prend le premier paquet
                for (int c = 0; c < 7; c++)
                {
                    place = 0;
                    if ((c == prem_paquet->pointeurs[0]))
                    {
                        etat_simu->valide_moi[c] += 1;
                        ordre[cpt] = c;
                        cpt++;
                        place++;
                    }
                    if (c == prem_paquet->pointeurs[1])
                    {
                        etat_simu->valide_moi[c] += 1;
                        ordre[cpt] = c;
                        cpt++;
                        place++;
                    }
                    for (int tmp = 0; tmp < cartes_choisis[c] - place; tmp++)
                    {
                        etat_simu->valide_adv[c] += 1;
                        ordre[cpt_adv] = c;
                        cpt_adv++;
                    }
                }
                if (!(cpt == 2 && cpt_adv == 4))
                {
                    printf("BOUCLE NON CORRECTE : %d %d", cpt, cpt_adv);
                    fflush(stdout);
                }
                assert(cpt == 2 && cpt_adv == 4);
                res = simulation_coup(tour_simu->n - tour_simu->k, cartes_simu, g.nb_restantes, g.restantes, g.act_poss[1], etat_simu, act_poss_simu);
                if (res < score_mini)
                {
                    score_mini = res;
                    coup_mini.cartes[0] = ordre[0];
                    coup_mini.cartes[1] = ordre[1];
                    coup_mini.cartes[2] = ordre[2];
                    coup_mini.cartes[3] = ordre[3];
                }

                etat_simu->valide_moi[ordre[0]] -= 1;
                etat_simu->valide_moi[ordre[1]] -= 1;
                etat_simu->valide_adv[ordre[2]] -= 1;
                etat_simu->valide_adv[ordre[3]] -= 1;
                // DEUXIEME POSSIBILITE : il prend le deuxième paquet
                etat_simu->valide_adv[ordre[0]] += 1;
                etat_simu->valide_adv[ordre[1]] += 1;
                etat_simu->valide_moi[ordre[2]] += 1;
                etat_simu->valide_moi[ordre[3]] += 1;

                res = simulation_coup(tour_simu->n - tour_simu->k, cartes_simu, g.nb_restantes, g.restantes, g.act_poss[1], etat_simu, act_poss_simu);
                if (res < score_mini)
                {
                    score_mini = res;
                    coup_mini.cartes[0] = ordre[2];
                    coup_mini.cartes[1] = ordre[3];
                    coup_mini.cartes[2] = ordre[0];
                    coup_mini.cartes[3] = ordre[1];
                }

                etat_simu->valide_adv[ordre[0]] -= 1;
                etat_simu->valide_adv[ordre[1]] -= 1;
                etat_simu->valide_moi[ordre[2]] -= 1;
                etat_simu->valide_moi[ordre[3]] -= 1;

                if (score_mini != 50 && score_mini > score_maxi)
                {
                    score_maxi = score_mini;
                    coup_maxi.action = coup_mini.action;
                    coup_maxi.cartes[0] = coup_mini.cartes[0];
                    coup_maxi.cartes[1] = coup_mini.cartes[1];
                    coup_maxi.cartes[2] = coup_mini.cartes[2];
                    coup_maxi.cartes[3] = coup_mini.cartes[3];
                }
                choix_cartes(prem_paquet);
            }
            free_marq(prem_paquet);

            ////// retour à l'état initial
            cartes_simu[tour_simu->pointeurs[0]] += 1;
            cartes_simu[tour_simu->pointeurs[1]] += 1;
            cartes_simu[tour_simu->pointeurs[2]] += 1;
            cartes_simu[tour_simu->pointeurs[3]] += 1;
            cartes_choisis[tour_simu->pointeurs[0]] -= 1;
            cartes_choisis[tour_simu->pointeurs[1]] -= 1;
            cartes_choisis[tour_simu->pointeurs[2]] -= 1;
            cartes_choisis[tour_simu->pointeurs[3]] -= 1;
            choix_cartes(tour_simu);
        }
        // désalocation de la mémoire
        free_marq(tour_simu);
        free(ordre);
        free(cartes_choisis);
        act_poss_simu[3] = true;
    }
    printf("FIN SIMU : %d\n", coup_maxi.action);
    // Joue l'action
    if (coup_maxi.action == 1)
    {
        joue_valide(coup_maxi.cartes[0]);
    }
    else if (coup_maxi.action == 2)
    {
        joue_defausse(coup_maxi.cartes[0], coup_maxi.cartes[1]);
    }
    else if (coup_maxi.action == 3)
    {
        joue_trois(coup_maxi.cartes[0], coup_maxi.cartes[1], coup_maxi.cartes[2]);
    }
    else if (coup_maxi.action == 4)
    {
        joue_quatre(coup_maxi.cartes[0], coup_maxi.cartes[1], coup_maxi.cartes[2], coup_maxi.cartes[3]);
    }
    else
    {
        printf("ERREUR ! AUCUNE ACTION JOUEE :\n");
    }
    // Désallocation de la mémoire
    free(coup_mini.cartes);
    free(coup_maxi.cartes);
    free(cartes_simu);
    free(etat_simu->avantage);
    free(etat_simu->valide_adv);
    free(etat_simu->valide_moi);
    free(etat_simu);
    free(act_poss_simu);
    printf("SCORE : %f\nTEMPS : %ld ms\n\n######################################\n\n", score_maxi, currenttime() - t1);
}

// Fonction appelée lors du choix entre les trois cartes lors de l'action de
// l'adversaire (cf tour_precedent)
void repondre_action_choix_trois(void)
{
    // INITIALISATION
    printf("Repondre choix 3\n");
    t1 = currenttime();
    update(false);
    debug_cartes(7, g.cartes, "Mes cartes");
    debug_cartes(7, g.restantes, "Cartes restantes");
    action_jouee tp = tour_precedent();
    int cartes_3[3] = {tp.c1, tp.c2, tp.c3};

    float score_maxi = -50;
    int coup_max;
    float res;

    ETAT *etat_simu = malloc(sizeof(ETAT));
    int *restantes_simu = malloc(7 * sizeof(int));
    etat_simu->avantage = malloc(7 * sizeof(int));
    etat_simu->valide_adv = malloc(7 * sizeof(int));
    etat_simu->valide_moi = malloc(7 * sizeof(int));
    for (int c = 0; c < 7; c++)
    {
        restantes_simu[c] = g.restantes[c];
        etat_simu->avantage[c] = g.etat->avantage[c];
        etat_simu->valide_adv[c] = g.etat->valide_adv[c];
        etat_simu->valide_moi[c] = g.etat->valide_moi[c];
    }
    for (int c = 0; c < 3; c++)
    {
        restantes_simu[cartes_3[c]] -= 1;
    }
    debug_cartes(7, restantes_simu, "Restantes_simu");

    // On va simuler si on prend chaqu'une des possibilités
    for (int carte_choisie = 0; carte_choisie < 3; carte_choisie++)
    {
        etat_simu->valide_moi[cartes_3[carte_choisie]] += 1;
        etat_simu->valide_adv[cartes_3[permu_trois[carte_choisie][0]]] += 1;
        etat_simu->valide_adv[cartes_3[permu_trois[carte_choisie][1]]] += 1;
        res = simulation_coup(g.en_main, g.cartes, g.nb_restantes - 3, restantes_simu, g.act_poss[1], etat_simu, g.act_poss);

        if (res > score_maxi)
        {
            score_maxi = res;
            coup_max = carte_choisie;
        }
        etat_simu->valide_moi[cartes_3[carte_choisie]] -= 1;
        etat_simu->valide_adv[cartes_3[permu_trois[carte_choisie][0]]] -= 1;
        etat_simu->valide_adv[cartes_3[permu_trois[carte_choisie][1]]] -= 1;
    }
    // désallocation de mémoire
    free(restantes_simu);
    free(etat_simu->avantage);
    free(etat_simu->valide_adv);
    free(etat_simu->valide_moi);
    free(etat_simu);
    repondre_choix_trois(coup_max);
    printf("SCORE : %f\nTEMPS : %ld ms\n\n######################################\n\n", score_maxi, currenttime() - t1);
}

// Fonction appelée lors du choix entre deux paquet lors de l'action de
// l'adversaire (cf tour_precedent)
void repondre_action_choix_paquets(void)
{
    // INITIALISATION
    printf("Repondre choix paquets\n");
    t1 = currenttime();
    update(false);
    debug_cartes(7, g.cartes, "Mes cartes");
    debug_cartes(7, g.restantes, "Cartes restantes");
    action_jouee tp = tour_precedent();
    int cartes_4[4] = {tp.c1, tp.c2, tp.c3, tp.c4};

    float score_maxi = -50;
    int coup_max;
    float res;

    ETAT *etat_simu = malloc(sizeof(ETAT));
    int *restantes_simu = malloc(7 * sizeof(int));
    etat_simu->avantage = malloc(7 * sizeof(int));
    etat_simu->valide_adv = malloc(7 * sizeof(int));
    etat_simu->valide_moi = malloc(7 * sizeof(int));
    for (int c = 0; c < 7; c++)
    {
        restantes_simu[c] = g.restantes[c];
        etat_simu->avantage[c] = g.etat->avantage[c];
        etat_simu->valide_adv[c] = g.etat->valide_adv[c];
        etat_simu->valide_moi[c] = g.etat->valide_moi[c];
    }
    for (int c = 0; c < 4; c++)
    {
        restantes_simu[cartes_4[c]] -= 1;
    }
    debug_cartes(7, restantes_simu, "Restantes_simu");

    // On va tester si on prend chaqu'un des deux paquets
    for (int carte_choisie = 0; carte_choisie < 2; carte_choisie++)
    {
        etat_simu->valide_moi[cartes_4[permu_paquet[carte_choisie][0]]] += 1;
        etat_simu->valide_moi[cartes_4[permu_paquet[carte_choisie][1]]] += 1;
        etat_simu->valide_adv[cartes_4[permu_paquet[carte_choisie][2]]] += 1;
        etat_simu->valide_adv[cartes_4[permu_paquet[carte_choisie][3]]] += 1;
        res = simulation_coup(g.en_main, g.cartes, g.nb_restantes - 4, restantes_simu, g.act_poss[1], etat_simu, g.act_poss);

        if (res > score_maxi)
        {
            score_maxi = res;
            coup_max = carte_choisie;
        }
        etat_simu->valide_moi[cartes_4[permu_paquet[carte_choisie][0]]] -= 1;
        etat_simu->valide_moi[cartes_4[permu_paquet[carte_choisie][1]]] -= 1;
        etat_simu->valide_adv[cartes_4[permu_paquet[carte_choisie][2]]] -= 1;
        etat_simu->valide_adv[cartes_4[permu_paquet[carte_choisie][3]]] -= 1;
    }
    // désalocation de la mémoire
    free(restantes_simu);
    free(etat_simu->avantage);
    free(etat_simu->valide_adv);
    free(etat_simu->valide_moi);
    free(etat_simu);
    repondre_choix_paquets(coup_max);
    printf("SCORE : %f\nTEMPS : %ld ms\n\n######################################\n\n", score_maxi, currenttime() - t1);
}

// Fonction appelée à la fin du jeu
void fin_jeu(void)
{
    // Désallocation de la mémoire
    free(g.cartes);
    free(g.etat->valide_adv);
    free(g.etat->valide_moi);
    free(g.etat->avantage);
    free(g.etat);
    free(g.act_poss);
    free(g.restantes);
    printf("Fin\n");
}
