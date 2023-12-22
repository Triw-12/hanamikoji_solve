let nb_geisha = 7
(** Les 7 Geisha (2, 2, 2, 3, 3, 4, 5) *)

let nb_cartes_totales = 21
(** Le nombre total de cartes (2 + 2 + 2 + 3 + 3 + 4 + 5) *)

let nb_cartes_debut = 6
(** Le nombre de cartes que chaque personne a au début *)

let nb_cartes_ecartees = 1
(** Le nombre de cartes écartées au début du jeu *)

let nb_actions = 4
(** Le nombre total d'actions que chaque joueur devra faire *)

let nb_manches_max = 3
(** Le nombre total de manches avant la fin de la partie *)

let geisha_valeur = "2|2|2|3|3|4|5"
(** La valeur (et le nombre de cartes) de chaque Geisha séparée par des | *)


(** Les actions de jeu *)
type action =
  | Valider (** <- Valide une unique carte *)
  | Defausser (** <- Défausse deux cartes *)
  | Choix_trois (** <- Donne le choix entre trois cartes *)
  | Choix_paquets (** <- Donne le choix entre deux paquets de deux cartes *)
  | Premier_joueur (** <- Aucune action n'a été jouée (utilisé dans tour_precedent) *)

(** Enumeration contentant toutes les erreurs possibles *)
type error =
  | Ok (** <- pas d'erreur *)
  | Action_deja_jouee (** <- l'action a déjà été jouée *)
  | Cartes_invalides (** <- vous ne pouvez pas jouer ces cartes *)
  | Paquet_invalide (** <- ce paquet n'existe pas *)
  | Geisha_invalides (** <- cette Geisha n'existe pas (doit être un entier entre 0 et NB_GEISHA - 1) *)
  | Joueur_invalide (** <- ce joueur n'existe pas *)
  | Choix_invalide (** <- vous ne pouvez pas répondre à ce choix *)
  | Action_invalide (** <- vous ne pouvez pas jouer cette action maintenant *)

(** Enumeration représentant les différents joueurs *)
type joueur =
  | Joueur_1 (** <- Le joueur 1 *)
  | Joueur_2 (** <- Le joueur 2 *)
  | Egalite (** <- Égalité, utilisé uniquement dans possession_geisha *)


(** La description d'une action jouée *)
type action_jouee = {
  act : action; (** <- L'action jouée *)
  c1 : int; (** <- Si act==VALIDER ou act==DEFAUSSER, -1 sinon la première carte (du premier paquet) *)
  c2 : int; (** <- Si act==V|D: -1 sinon la deuxième carte (du premier paquet) *)
  c3 : int; (** <- Si act==V|D: -1 sinon la troisième carte (ou la première carte du second paquet si act==choix paquet) *)
  c4 : int; (** <- Si act!=choix paquet: -1 sinon la deuxième carte du second paquet *)
}

external id_joueur : unit -> joueur = "ml_id_joueur"
(** Renvoie l'identifiant du joueur *)

external id_adversaire : unit -> joueur = "ml_id_adversaire"
(** Renvoie l'identifiant de l'adversaire *)

external manche : unit -> int = "ml_manche"
(** Renvoie le numéro de la manche (entre 0 et 2) *)

external tour : unit -> int = "ml_tour"
(** Renvoie le numéro du tour (entre 0 et 7) *)

external tour_precedent : unit -> action_jouee = "ml_tour_precedent"
(** Renvoie l'action jouée par l'adversaire *)

external nb_cartes_validees : joueur -> int -> int = "ml_nb_cartes_validees"
(** Renvoie le nombre de cartes validées par le joueur pour la Geisha (la carte
 ** validée secrètement n'est pas prise en compte) *)

external possession_geisha : int -> joueur = "ml_possession_geisha"
(** Renvoie qui possède la Geisha *)

external est_jouee_action : joueur -> action -> bool = "ml_est_jouee_action"
(** Renvoie si l'action a déjà été jouée par le joueur *)

external nb_cartes : joueur -> int = "ml_nb_cartes"
(** Renvoie le nombre de cartes que le joueur a *)

external cartes_en_main : unit -> int array = "ml_cartes_en_main"
(** Renvoie les cartes que vous avez *)

external carte_piochee : unit -> int = "ml_carte_piochee"
(** Renvoie la carte que vous avez piochée au début du tour *)

external action_valider : int -> error = "ml_action_valider"
(** Jouer l'action valider une carte *)

external action_defausser : int -> int -> error = "ml_action_defausser"
(** Jouer l'action défausser deux cartes *)

external action_choix_trois : int -> int -> int -> error = "ml_action_choix_trois"
(** Jouer l'action choisir entre trois cartes *)

external action_choix_paquets : int -> int -> int -> int -> error = "ml_action_choix_paquets"
(** Jouer l'action choisir entre deux paquets de deux cartes *)

external repondre_choix_trois : int -> error = "ml_repondre_choix_trois"
(** Choisir une des trois cartes proposées. *)

external repondre_choix_paquets : int -> error = "ml_repondre_choix_paquets"
(** Choisir un des deux paquets proposés. *)

external afficher_action : action -> unit = "ml_afficher_action"
(** Affiche le contenu d'une valeur de type action *)

external afficher_error : error -> unit = "ml_afficher_error"
(** Affiche le contenu d'une valeur de type error *)

external afficher_joueur : joueur -> unit = "ml_afficher_joueur"
(** Affiche le contenu d'une valeur de type joueur *)

external afficher_action_jouee : action_jouee -> unit = "ml_afficher_action_jouee"
(** Affiche le contenu d'une valeur de type action_jouee *)

