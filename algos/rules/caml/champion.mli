
val init_jeu : unit -> unit
(** Fonction appelée au début du jeu *)

val jouer_tour : unit -> unit
(** Fonction appelée au début du tour *)

val repondre_action_choix_trois : unit -> unit
(** Fonction appelée lors du choix entre les trois cartes lors de l'action de
 ** l'adversaire (cf tour_precedent) *)

val repondre_action_choix_paquets : unit -> unit
(** Fonction appelée lors du choix entre deux paquet lors de l'action de
 ** l'adversaire (cf tour_precedent) *)

val fin_jeu : unit -> unit
(** Fonction appelée à la fin du jeu *)
