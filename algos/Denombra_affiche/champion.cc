#include <algorithm>
#include <cassert>
#include <chrono>

#include "api.hh"
#include "combinaisons.hh"
#include "context.hh"

using namespace std;

Context ctx;

/// Fonction appelée au début du jeu
void init_jeu() { ctx.init(); }

/// Fonction appelée au début du tour
void jouer_tour() {
  auto t1 = std::chrono::high_resolution_clock::now();
  ctx.jouer_tour();
  auto t2 = std::chrono::high_resolution_clock::now();
  std::chrono::duration<double, std::milli> ms_double = t2 - t1;
  printf("Joueur tour %fms\n", ms_double.count());
}

/// Fonction appelée lors du choix entre les trois cartes lors de l'action de
/// l'adversaire (cf tour_precedent)
void repondre_action_choix_trois() {
  action_jouee aj = tour_precedent();
  assert(aj.act == CHOIX_TROIS);
  ctx.repondre_trois(aj.c1, aj.c2, aj.c3);
}

/// Fonction appelée lors du choix entre deux paquet lors de l'action de
/// l'adversaire (cf tour_precedent)
void repondre_action_choix_paquets() {
  action_jouee aj = tour_precedent();
  assert(aj.act == CHOIX_PAQUETS);
  ctx.repondre_paquets(aj.c1, aj.c2, aj.c3, aj.c4);
}

/// Fonction appelée à la fin du jeu
void fin_jeu() {
  // TODO
}
