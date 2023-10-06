#include "combinaisons.hh"

#include <algorithm>
#include <cassert>
#include <cstdio>
#include <vector>

#include "api.hh"

vector<int> cartes_to_vector(Cartesptr cartes, int nb) {
  vector<int> vec(nb);
  if (nb < 0) {
    for (int g = 0; g < NB_GEISHA; g++) {
      for (int j = 0; j < cartes[g]; j++) {
        vec.push_back(g);
      }
    }
  } else {
    int id = 0;
    for (int g = 0; g < NB_GEISHA; g++) {
      for (int j = 0; j < cartes[g]; j++) {
        vec[id++] = g;
      }
    }
  }
  return vec;
}

void print_cartes(int *cartes) {
  for (int g = 0; g < NB_GEISHA; g++) {
    printf("%d ", cartes[g]);
  }
  printf("\n");
}

CombinaisonIterator::CombinaisonIterator(const Cartes &c, int nb)
    : cartes_(c), nb_(nb), is_finished_(false) {
  assert(nb <= MAX_NB);

  fill_n(cartes_courantes_, NB_GEISHA, 0);
  int g = 0;
  for (int i = 0; i < nb; i++) {
    while (cartes_courantes_[g] >= cartes_[g]) {
      g++;
      if (g >= NB_GEISHA) {
        is_finished_ = true;
        return;
      }
    }

    idx_[i] = g;
    cartes_courantes_[g]++;
  }

  Cartes cc;
  g = NB_GEISHA - 1;
  fill_n(cc, NB_GEISHA, 0);
  for (int i = nb - 1; i >= 0; i--) {
    while (cc[g] >= cartes_[g]) {
      g--;
      assert(g >= 0);
    }
    last_idx_[i] = g;
    cc[g] += 1;
  }
}

Cartesptr CombinaisonIterator::suiv() {
  if (is_finished_) return nullptr;

  copy_n(cartes_courantes_, NB_GEISHA, cartes_returned_);

  int i = nb_ - 1;
  while (i >= 0 && idx_[i] >= last_idx_[i]) {
    i--;
  }

  if (i < 0) {
    is_finished_ = true;
    return cartes_returned_;
  }

  for (int j = i; j < nb_; j++) {
    cartes_courantes_[idx_[j]]--;
  }

  int g = idx_[i] + 1;
  while (cartes_[g] < 1) g++;

  assert(0 <= g && g < NB_GEISHA);
  idx_[i] = g;
  cartes_courantes_[g]++;

  for (int j = i + 1; j < nb_; j++) {
    while (cartes_courantes_[g] >= cartes_[g]) {
      g++;
      assert(g < NB_GEISHA);
    }
    cartes_courantes_[g]++;
    idx_[j] = g;
  }

  return cartes_returned_;
}