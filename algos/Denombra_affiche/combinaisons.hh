#pragma once
#include "api.hh"
using namespace std;

typedef int Cartes[NB_GEISHA];
#define MAX_NB 21

vector<int> cartes_to_vector(Cartesptr cts, int nb = 0);
void print_cartes(int* cartes);

class CombinaisonIterator {
 public:
  CombinaisonIterator(const Cartes& cartes, int nb);

  Cartesptr suiv();

 private:
  int idx_[MAX_NB];
  int last_idx_[MAX_NB];
  Cartes cartes_courantes_;
  Cartes cartes_returned_;
  const Cartes& cartes_;
  const int nb_;
  bool is_finished_;
};