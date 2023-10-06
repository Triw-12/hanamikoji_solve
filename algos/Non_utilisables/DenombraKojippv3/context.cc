#include "context.hh"

#include <math.h>

#include <algorithm>
#include <cassert>
#include <cmath>
#include <cstdio>
#include <limits>
#include <vector>

#include "api.hh"
#include "combinaisons.hh"

Context::Context() {}

void Context::init() {
  manche_ = -1;
  moi_ = id_joueur();
  adv_ = id_adversaire();

  printf("Denimbrakoji++ v3, joueur %d\n", moi_);
}

void Context::update() {
  const int m = manche();
  if (m != manche_) {
    valide_secretement_ = -1;
    fill_n(defausse_secretement_, 2, -1);
    manche_ = m;
  }
  tour_ = tour();
  main_ = cartes_en_main();
  printf("\n# %d %d\n", manche_, tour_);

  fill_n(main_count_, NB_GEISHA, 0);
  for (int c : main_) {
    main_count_[c] += 1;
  }

  for (int g = 0; g < NB_GEISHA; g++) {
    cartes_moi_[g] = nb_cartes_validees(moi_, g);
    cartes_adv_[g] = nb_cartes_validees(adv_, g);
    possession_geisha_[g] = possession_geisha(g);
  }

  if (valide_secretement_ >= 0) {
    cartes_moi_[valide_secretement_]++;
  }

  for (int a = 0; a < NB_ACTIONS; a++) {
    actions_moi_[a] = !est_jouee_action(moi_, static_cast<action>(a));
    actions_adv_[a] = !est_jouee_action(adv_, static_cast<action>(a));
  }

  updateRemaining();
}

void Context::updateRemaining() {
  copy_n(GEISHA_VALEUR_INT, NB_GEISHA, cartes_restantes_);
  copy_n(GEISHA_VALEUR_INT, NB_GEISHA, cartes_restantes_adv_);

  for (int g = 0; g < NB_GEISHA; g++) {
    const int tot = cartes_moi_[g] + cartes_adv_[g];
    cartes_restantes_[g] -= tot;
    cartes_restantes_adv_[g] -= tot + main_count_[g];
  }
  if (defausse_secretement_[0] >= 0) {
    cartes_restantes_[defausse_secretement_[0]]--;
    cartes_restantes_adv_[defausse_secretement_[0]]--;
    cartes_restantes_[defausse_secretement_[1]]--;
    cartes_restantes_adv_[defausse_secretement_[1]]--;
  }
}

void Context::jouer_tour() {
  update();
  estimation_type best_estimation = -INFINITY;
  int best_action = -1;
  vector<int> best_cartes(4);

  for (int a = 0; a < NB_ACTIONS; a++) {
    if (!actions_moi_[a]) continue;

    CombinaisonIterator cit(main_count_, a + 1);
    Cartesptr c;
    while ((c = cit.suiv()) != nullptr) {
      vector<int> cartes = cartes_to_vector(c, a + 1);
      estimation_type ev;
      switch (a) {
        case 0:
          ev = estimation_valider(cartes[0]);
          break;
        case 1:
          ev = estimation_defausser(cartes[0], cartes[1]);
          break;
        case 2:
          ev = estimation_choix_trois(cartes[0], cartes[1], cartes[2]);
          break;
        case 3:
          ev = estimation_choix_paquets(cartes[0], cartes[1], cartes[2],
                                        cartes[3]);
          int choice = 0;
          estimation_type nev = estimation_choix_paquets(cartes[0], cartes[2],
                                                         cartes[1], cartes[3]);
          if (nev > ev) {
            choice = 1;
            ev = nev;
          }

          nev = estimation_choix_paquets(cartes[0], cartes[3], cartes[1],
                                         cartes[2]);
          if (nev > ev) {
            choice = 2;
            ev = nev;
          }

          if (choice == 1) {
            int temp = cartes[2];
            cartes[2] = cartes[1];
            cartes[1] = temp;
          } else if (choice == 2) {
            int temp = cartes[3];
            cartes[3] = cartes[1];
            cartes[1] = temp;
          }
          break;
      }

      if (ev > best_estimation) {
        best_action = a;
        best_estimation = ev;
        for (int i = 0; i <= a; i++) {
          best_cartes[i] = cartes[i];
        }
      }
    }
  }

  printf("%d: Meilleure estimation: %f !\n", moi_, best_estimation);

  switch (best_action) {
    case 0:
      valider_cartes(best_cartes[0]);
      break;
    case 1:
      defausser_cartes(best_cartes[0], best_cartes[1]);
      break;
    case 2:
      choix_trois_cartes(best_cartes[0], best_cartes[1], best_cartes[2]);
      break;
    case 3:
      choix_paquets_cartes(best_cartes[0], best_cartes[1], best_cartes[2],
                           best_cartes[3]);
      break;
  }
}

void Context::repondre_trois(int c1, int c2, int c3) {
  update();
  cartes_moi_[c1]++;
  cartes_moi_[c2]++;
  cartes_adv_[c3]++;
  int choix = 0;
  estimation_type ev = estimation();
  cartes_moi_[c2]--;
  cartes_adv_[c3]--;

  cartes_adv_[c2]++;
  cartes_moi_[c3]++;
  estimation_type nev = estimation();
  if (nev > ev) {
    choix = 1;
    ev = nev;
  }

  cartes_moi_[c1]--;
  cartes_adv_[c2]--;

  cartes_adv_[c1]++;
  cartes_moi_[c2]++;
  nev = estimation();
  if (nev > ev) {
    choix = 2;
  }

  cartes_adv_[c1]--;
  cartes_moi_[c2]--;
  cartes_moi_[c3]--;

  repondre_choix_trois_cartes(choix);
}

void Context::repondre_paquets(int c1, int c2, int c3, int c4) {
  update();
  cartes_moi_[c1]++;
  cartes_moi_[c2]++;
  cartes_adv_[c3]++;
  cartes_adv_[c4]++;
  int choix = 0;
  estimation_type ev = estimation();
  cartes_moi_[c1]--;
  cartes_moi_[c2]--;
  cartes_adv_[c3]--;
  cartes_adv_[c4]--;

  cartes_adv_[c1]++;
  cartes_adv_[c2]++;
  cartes_moi_[c3]++;
  cartes_moi_[c4]++;
  estimation_type nev = estimation();
  if (nev > ev) {
    choix = 1;
  }
  cartes_adv_[c1]--;
  cartes_adv_[c2]--;
  cartes_moi_[c3]--;
  cartes_moi_[c4]--;

  repondre_choix_paquets_cartes(choix);
}

int Context::raw_estimation() {
  int score_moi = 0;
  int score_adv = 0;
  int nb_c_moi = 0;
  int nb_c_adv = 0;

  for (int g = 0; g < NB_GEISHA; g++) {
    if (cartes_moi_[g] > cartes_adv_[g]) {
      score_moi += GEISHA_VALEUR_INT[g];
      nb_c_moi++;
    } else if (cartes_adv_[g] > cartes_moi_[g]) {
      score_adv += GEISHA_VALEUR_INT[g];
      nb_c_adv++;
    } else if (possession_geisha_[g] == moi_) {
      score_moi += GEISHA_VALEUR_INT[g];
      nb_c_moi++;
    } else if (possession_geisha_[g] == adv_) {
      score_adv += GEISHA_VALEUR_INT[g];
      nb_c_adv++;
    }
  }

  if (score_moi >= 11) {
    return 21;
  } else if (score_adv >= 11) {
    return -21;
  } else if (nb_c_moi >= 4) {
    return 20;
  } else if (nb_c_adv >= 4) {
    return -20;
  } else {
    return score_moi - score_adv;
  }
}
estimation_type Context::estimation() {
  updateRemaining();

  int min_estimation = numeric_limits<int>::max();
  int count = 0;
  int total_ev = 0;
  const int nb = nb_cartes_valides_potentielle_moi();
  Cartes ccc;
  copy_n(cartes_restantes_, NB_GEISHA, ccc);
  CombinaisonIterator cit(ccc, nb);

  Cartesptr c;
  while ((c = cit.suiv()) != nullptr) {
    // printf(
    //     "Status: c, main_count_, cartes_moi_, cartes_adv_, "
    //     "cartes_restantes_, "
    //     "cartes_restantes_adv_\n");
    // print_cartes(c);
    // print_cartes(main_count_);
    // print_cartes(cartes_moi_);
    // print_cartes(cartes_adv_);
    // print_cartes(cartes_restantes_);
    // print_cartes(cartes_restantes_adv_);
    int nb_main_moi =
        2 * (actions_moi_[CHOIX_TROIS] + actions_moi_[CHOIX_PAQUETS]) +
        actions_moi_[VALIDER];

    int nb_main_moi_max = nb_main_moi;

    const int nb_actions_moi = actions_moi_[VALIDER] + actions_moi_[DEFAUSSER] +
                               actions_moi_[CHOIX_TROIS] +
                               actions_moi_[CHOIX_PAQUETS];

    int max_potential_main_card = 0;
    for (int g = 0; g < NB_GEISHA; g++) {
      cartes_restantes_[g] -= c[g];
      cartes_moi_[g] += c[g];
      nb_main_moi_max -= max(0, c[g] - cartes_restantes_adv_[g]);
      max_potential_main_card += min(main_count_[g], c[g]);
      assert(0 <= cartes_moi_[g] && cartes_moi_[g] <= GEISHA_VALEUR_INT[g]);
      assert(0 <= cartes_restantes_[g] &&
             cartes_restantes_[g] <= GEISHA_VALEUR_INT[g]);
    }

    // On choisit les trois cartes qu'il ne peut
    // pas avoir (sa défausse + la carte inconnue)
    CombinaisonIterator cit2(cartes_restantes_, 3);
    Cartesptr c2;

    if (nb_main_moi_max < 0 ||
        nb_main_moi - max_potential_main_card > nb_actions_moi)
      goto cleanup_c;

    while ((c2 = cit2.suiv()) != nullptr) {
      int nb_main_adv =
          actions_moi_[CHOIX_TROIS] + 2 * actions_moi_[CHOIX_PAQUETS];
      int nb_main_adv_max = nb_main_adv;

      int max_potential_main_card = 0;
      for (int g = 0; g < NB_GEISHA; g++) {
        int nb = cartes_restantes_[g] - c2[g];
        cartes_adv_[g] += nb;
        assert(0 <= cartes_adv_[g] && cartes_adv_[g] <= GEISHA_VALEUR_INT[g]);
        nb_main_adv_max -= max(nb - cartes_restantes_adv_[g], 0);
        max_potential_main_card += min(main_count_[g], nb);
      }
      int ev;
      if (nb_main_adv_max < 0 ||
          nb_main_adv - max_potential_main_card > nb_actions_moi)
        goto cleanup_c2;

      ev = raw_estimation();
      if (ev < min_estimation) {
        min_estimation = ev;
      }
      total_ev += ev;
      count++;

    cleanup_c2:
      for (int g = 0; g < NB_GEISHA; g++) {
        cartes_adv_[g] -= cartes_restantes_[g] - c2[g];
        assert(0 <= cartes_adv_[g] && cartes_adv_[g] <= GEISHA_VALEUR_INT[g]);
      }
    }

  cleanup_c:

    for (int g = 0; g < NB_GEISHA; g++) {
      cartes_restantes_[g] += c[g];
      cartes_moi_[g] -= c[g];
      // assert(0 <= cartes_moi_[g] && cartes_moi_[g] <= GEISHA_VALEUR_INT[g]);
      // assert(0 <= cartes_restantes_[g] &&
      //        cartes_restantes_[g] <= GEISHA_VALEUR_INT[g]);
    }
  }

  assert(count > 0);

  float final_ev = (float)total_ev / count;

  bool are_wining =
      min_estimation >= 20 || (manche_ == 2 && min_estimation > 0);
  return are_wining ? final_ev + 21 : final_ev;
}

inline estimation_type Context::estimation_valider(int c) {
  // assert(actions_moi_[VALIDER]);
  actions_moi_[VALIDER] = false;
  main_to_moi(c);
  estimation_type ev = estimation();
  moi_to_main(c);
  actions_moi_[VALIDER] = true;
  return ev;
}

inline estimation_type Context::estimation_defausser(int c1, int c2) {
  // assert(actions_moi_[DEFAUSSER]);
  actions_moi_[DEFAUSSER] = false;
  main_count_[c1]--;
  main_count_[c2]--;
  defausse_secretement_[0] = c1;
  defausse_secretement_[1] = c2;
  estimation_type ev = estimation();
  defausse_secretement_[0] = -1;
  defausse_secretement_[1] = -1;
  main_count_[c1]++;
  main_count_[c2]++;
  actions_moi_[DEFAUSSER] = true;
  return ev;
}

inline estimation_type Context::estimation_choix_trois(int c1, int c2, int c3) {
  // assert(actions_moi_[CHOIX_TROIS]);
  actions_moi_[CHOIX_TROIS] = false;
  main_to_moi(c1);
  main_to_moi(c2);
  main_to_adv(c3);
  estimation_type ev = estimation();
  moi_to_main(c1);
  moi_to_main(c2);
  adv_to_main(c3);
  main_to_moi(c1);
  main_to_adv(c2);
  main_to_moi(c3);
  estimation_type nev = estimation();
  if (nev < ev) {
    ev = nev;
  }
  moi_to_main(c1);
  adv_to_main(c2);
  moi_to_main(c3);

  main_to_adv(c1);
  main_to_moi(c2);
  main_to_moi(c3);
  nev = estimation();
  if (nev < ev) {
    ev = nev;
  }
  adv_to_main(c1);
  moi_to_main(c2);
  moi_to_main(c3);

  actions_moi_[CHOIX_TROIS] = true;
  return ev;
}

inline estimation_type Context::estimation_choix_paquets(int c1, int c2, int c3,
                                                         int c4) {
  // assert(actions_moi_[CHOIX_PAQUETS]);
  actions_moi_[CHOIX_PAQUETS] = false;
  main_to_moi(c1);
  main_to_moi(c2);
  main_to_adv(c3);
  main_to_adv(c4);
  estimation_type ev = estimation();
  moi_to_main(c1);
  moi_to_main(c2);
  adv_to_main(c3);
  adv_to_main(c4);
  main_to_adv(c1);
  main_to_adv(c2);
  main_to_moi(c3);
  main_to_moi(c4);
  estimation_type nev = estimation();
  if (nev < ev) {
    ev = nev;
  }
  adv_to_main(c1);
  adv_to_main(c2);
  moi_to_main(c3);
  moi_to_main(c4);

  actions_moi_[CHOIX_PAQUETS] = true;
  return ev;
}

inline void Context::main_to_moi(int c) {
  main_count_[c]--;
  cartes_moi_[c]++;
}
inline void Context::main_to_adv(int c) {
  main_count_[c]--;
  cartes_adv_[c]++;
}
inline void Context::moi_to_main(int c) {
  cartes_moi_[c]--;
  main_count_[c]++;
}
inline void Context::adv_to_main(int c) {
  cartes_adv_[c]--;
  main_count_[c]++;
}
inline void Context::moi_to_adv(int c) {
  cartes_moi_[c]--;
  cartes_adv_[c]++;
}
inline void Context::adv_to_moi(int c) {
  cartes_adv_[c]--;
  cartes_moi_[c]++;
}

inline int Context::nb_cartes_valides_potentielle_moi() {
  return 1 * actions_moi_[VALIDER] + 2 * actions_moi_[CHOIX_TROIS] +
         2 * actions_moi_[CHOIX_PAQUETS] + 1 * actions_adv_[CHOIX_TROIS] +
         2 * actions_adv_[CHOIX_PAQUETS];
}

inline int Context::nb_cartes_valides_potentielle_adv() {
  return 1 + 2 * actions_adv_[CHOIX_TROIS] + 2 * actions_adv_[CHOIX_PAQUETS] +
         1 * actions_moi_[CHOIX_TROIS] + 2 * actions_moi_[CHOIX_PAQUETS];
}

#define AFFICHER_ERR(f) afficher_error(f)

inline void Context::valider_cartes(int c) {
  assert(actions_moi_[VALIDER]);
  valide_secretement_ = c;
  AFFICHER_ERR(action_valider(c));
  printf("%d: Je valide %d\n", moi_, c);
}
inline void Context::defausser_cartes(int c1, int c2) {
  assert(actions_moi_[DEFAUSSER]);
  defausse_secretement_[0] = c1;
  defausse_secretement_[1] = c2;
  AFFICHER_ERR(action_defausser(c1, c2));
  printf("%d: Je defausse %d %d\n", moi_, c1, c2);
}
inline void Context::choix_trois_cartes(int c1, int c2, int c3) {
  assert(actions_moi_[CHOIX_TROIS]);
  AFFICHER_ERR(action_choix_trois(c1, c2, c3));
  printf("%d: Choix trois %d %d %d\n", moi_, c1, c2, c3);
}
inline void Context::choix_paquets_cartes(int p1c1, int p1c2, int p2c1,
                                          int p2c2) {
  assert(actions_moi_[CHOIX_PAQUETS]);
  AFFICHER_ERR(action_choix_paquets(p1c1, p1c2, p2c1, p2c2));
  printf("%d: Choix paquets (%d %d) (%d %d)\n", moi_, p1c1, p1c2, p2c1, p2c2);
}

inline void Context::repondre_choix_trois_cartes(int c) {
  AFFICHER_ERR(repondre_choix_trois(c));
  printf("%d: Réponse choix trois %d\n", moi_, c);
}

inline void Context::repondre_choix_paquets_cartes(int p) {
  AFFICHER_ERR(repondre_choix_paquets(p));
  printf("%d: Réponse choix paquets %d\n", moi_, p);
}