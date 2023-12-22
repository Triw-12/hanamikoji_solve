open Api


let init_jeu () : unit =
(** Fonction appelée au début du jeu *)
    (* TODO *)

    (* Pour s'assurer que les sorties s'affichent *)
    flush stderr;
    flush stdout

let jouer_tour () : unit =
(** Fonction appelée au début du tour *)
    (* TODO *)

    (* Pour s'assurer que les sorties s'affichent *)
    flush stderr;
    flush stdout

let repondre_action_choix_trois () : unit =
(** Fonction appelée lors du choix entre les trois cartes lors de l'action de
 ** l'adversaire (cf tour_precedent) *)
    (* TODO *)

    (* Pour s'assurer que les sorties s'affichent *)
    flush stderr;
    flush stdout

let repondre_action_choix_paquets () : unit =
(** Fonction appelée lors du choix entre deux paquets lors de l'action de
 ** l'adversaire (cf tour_precedent) *)
    (* TODO *)

    (* Pour s'assurer que les sorties s'affichent *)
    flush stderr;
    flush stdout

let fin_jeu () : unit =
(** Fonction appelée à la fin du jeu *)
    (* TODO *)

    (* Pour s'assurer que les sorties s'affichent *)
    flush stderr;
    flush stdout

(* /!\ Ne modifie pas les lignes suivantes, elles sont importantes pour
** l'utilisation du moteur de jeu /!\ *)
let _ =
    Callback.register "ml_init_jeu" init_jeu;
    Callback.register "ml_jouer_tour" jouer_tour;
    Callback.register "ml_repondre_action_choix_trois" repondre_action_choix_trois;
    Callback.register "ml_repondre_action_choix_paquets" repondre_action_choix_paquets;
    Callback.register "ml_fin_jeu" fin_jeu
