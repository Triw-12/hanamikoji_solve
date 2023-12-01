#pragma once
#include <vector>

#include "api.hh"
#include "combinaisons.hh"
using namespace std;

typedef float estimation_type;

class Context {
 public:
  Context();
  void init();
  void update();
  void updateRemaining();

  void jouer_tour();
  void repondre_trois(int c1, int c2, int c3);
  void repondre_paquets(int c1, int c2, int c3, int c4);

 private:
  estimation_type estimation();
  int raw_estimation();

  inline estimation_type estimation_valider(int c);
  inline estimation_type estimation_defausser(int c1, int c2);
  inline estimation_type estimation_choix_trois(int c1, int c2, int c3);
  inline estimation_type estimation_choix_paquets(int c1, int c2, int c3,
                                                  int c4);

  inline int nb_cartes_valides_potentielle_moi();
  inline int nb_cartes_valides_potentielle_adv();

  inline void main_to_moi(int c);
  inline void main_to_adv(int c);
  inline void moi_to_main(int c);
  inline void adv_to_main(int c);
  inline void moi_to_adv(int c);
  inline void adv_to_moi(int c);

  inline void valider_cartes(int c);
  inline void defausser_cartes(int c1, int c2);
  inline void choix_trois_cartes(int c1, int c2, int c3);
  inline void choix_paquets_cartes(int p1c1, int p1c2, int p2c1, int p2c2);
  inline void repondre_choix_trois_cartes(int c);
  inline void repondre_choix_paquets_cartes(int p);

  vector<int> main_;
  Cartes main_count_;
  Cartes cartes_moi_;
  Cartes cartes_adv_;
  Cartes cartes_restantes_;
  Cartes cartes_restantes_adv_;
  joueur possession_geisha_[NB_GEISHA];
  joueur moi_;
  joueur adv_;
  int manche_;
  int tour_;
  int valide_secretement_;
  int defausse_secretement_[2];
  bool actions_moi_[NB_ACTIONS];  // Les actions restantes
  bool actions_adv_[NB_ACTIONS];
};