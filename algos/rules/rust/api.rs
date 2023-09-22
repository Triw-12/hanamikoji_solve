// SPDX-License-Identifier: GPL-2.0-or-later
// Copyright (c) 2012-2020 Association Prologin <association@prologin.org>
//
// This file contains all the API functions for the Rust language, and all the
// constants, enumerations and structures.
//
// It has been generated. You can modify the end of the file if you want, but
// do not touch the part where constants, enums, structs, and api functions are
// defined.

//! Rust API for hanamikoji

use crate::ffi;
use crate::ffi::{array_of_borrow_to_c, CToRust, RustToC};

#[allow(unused_imports)]
use std::{cell::UnsafeCell, borrow::Borrow};

/// Les 7 geisha (2, 2, 2, 3, 3, 4, 5)
pub const NB_GEISHA: i32 = 7;

/// Le nombre total de cartes (2 + 2 + 2 + 3 + 3 + 4 + 5)
pub const NB_CARTES_TOTAL: i32 = 21;

/// Le nombre de cartes que chaque personne a au début
pub const NB_CARTES_DEBUT: i32 = 6;

/// Le nombre de cartes écartées au début du jeu
pub const NB_CARTES_ECARTEES: i32 = 1;

/// Le nombre total d'action que chaque joueur devra faire
pub const NB_ACTIONS: i32 = 4;

/// Le nombre total de manches avant la fin de la partie
pub const NB_MANCHES_MAX: i32 = 3;

/// La valeur (et le nombre de cartes) de chaque geisha séparée par des |
pub const GEISHA_VALEUR: &'static str = "2|2|2|3|3|4|5";

/// Les actions de jeu
#[derive(Clone, Copy, Debug, Eq, Hash, PartialEq, PartialOrd, Ord)]
pub enum Action {
    /// Valide une unique carte
    Valider,
    /// Defausse deux cartes
    Defausser,
    /// Donne le choix entre trois cartes
    ChoixTrois,
    /// Donne le choix entre deux paquets de deux cartes
    ChoixPaquets,
    /// Aucune action n'a été jouée (utilisé dans tour_precedent)
    PremierJoueur,
}

/// Enumeration contentant toutes les erreurs possibles
#[derive(Clone, Copy, Debug, Eq, Hash, PartialEq, PartialOrd, Ord)]
pub enum Error {
    /// pas d'erreur
    Ok,
    /// l'action a déjà été jouée
    ActionDejaJouee,
    /// vous ne pouvez pas jouer ces cartes
    CartesInvalides,
    /// ce paquet n'existe pas
    PaquetInvalide,
    /// cette geisha n'existe pas (doit être un entier entre 0 et NB_GEISHA)
    GeishaInvalides,
    /// ce joueur n'existe pas
    JoueurInvalide,
    /// vous ne pouvez pas repondre à ce choix
    ChoixInvalide,
    /// vous ne pouvez pas jouer cette action maintenant
    ActionInvalide,
}

/// Enumeration représentant les différents joueurs
#[derive(Clone, Copy, Debug, Eq, Hash, PartialEq, PartialOrd, Ord)]
pub enum Joueur {
    /// Le joueur 1
    Joueur1,
    /// Le joueur 2
    Joueur2,
    /// Égalité, utilisé uniquement dans possession_geisha
    Egalite,
}

/// La description d'une action jouée
#[derive(Clone, Copy, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
pub struct ActionJouee {
    /// L'action jouée
    pub act: Action,
    /// Si act==VALIDER ou act==DEFAUSSER, -1 sinon la première carte (du
    /// premier paquet)
    pub c1: i32,
    /// Si act==V|D: -1 sinon la deuxième carte (du premier paquet)
    pub c2: i32,
    /// Si act==V|D: -1 sinon la troisième carte (ou la première carte du
    /// second paquet si act==choix paquet)
    pub c3: i32,
    /// Si act!=choix paquet: -1 sinon la deuxième carte du second paquet
    pub c4: i32,
}


/// Renvoie l'identifiant du joueur
pub fn id_joueur() -> Joueur {
    unsafe {
        ffi::id_joueur().to_rust()
    }
}

/// Renvoie l'identifiant de l'adversaire
pub fn id_adversaire() -> Joueur {
    unsafe {
        ffi::id_adversaire().to_rust()
    }
}

/// Renvoie le numéro de la manche
pub fn manche() -> i32 {
    unsafe {
        ffi::manche().to_rust()
    }
}

/// Renvoie le numéro de la manche
pub fn tour() -> i32 {
    unsafe {
        ffi::tour().to_rust()
    }
}

/// Renvoie l'action jouée par l'adversaire
pub fn tour_precedent() -> ActionJouee {
    unsafe {
        ffi::tour_precedent().to_rust()
    }
}

/// Renvoie le nombre de carte validée par le joueur pour la geisha
///
/// ### Parameters
///  - `j`: Le joueur
///  - `g`: La geisha
pub fn nb_carte_validee(j: Joueur, g: i32) -> i32 {
    unsafe {
        let j = j.to_c();
        let g = g.to_c();
        ffi::nb_carte_validee(j, g).to_rust()
    }
}

/// Renvoie qui possède la geisha
///
/// ### Parameters
///  - `g`: La geisha
pub fn possession_geisha(g: i32) -> Joueur {
    unsafe {
        let g = g.to_c();
        ffi::possession_geisha(g).to_rust()
    }
}

/// Renvoie si l'action a déjà été jouée par le joueur
///
/// ### Parameters
///  - `j`: Le joueur
///  - `a`: L'action
pub fn est_jouee_action(j: Joueur, a: Action) -> bool {
    unsafe {
        let j = j.to_c();
        let a = a.to_c();
        ffi::est_jouee_action(j, a).to_rust()
    }
}

/// Renvoie le nombre de carte que le joueur a
///
/// ### Parameters
///  - `j`: Le joueur
pub fn nb_cartes(j: Joueur) -> i32 {
    unsafe {
        let j = j.to_c();
        ffi::nb_cartes(j).to_rust()
    }
}

/// Renvoie les cartes que vous avez
pub fn cartes_en_main() -> Vec<i32> {
    unsafe {
        ffi::cartes_en_main().to_rust()
    }
}

/// Renvoie la carte que vous avez pioché au début du tour
pub fn carte_pioche() -> i32 {
    unsafe {
        ffi::carte_pioche().to_rust()
    }
}

/// Jouer l'action valider une carte
///
/// ### Parameters
///  - `c`: La carte à jouer
pub fn action_valider(c: i32) -> Error {
    unsafe {
        let c = c.to_c();
        ffi::action_valider(c).to_rust()
    }
}

/// Jouer l'action défausser deux cartes
///
/// ### Parameters
///  - `c1`: La première carte à défausser
///  - `c2`: La deuxième carte à défausser
pub fn action_defausser(c1: i32, c2: i32) -> Error {
    unsafe {
        let c1 = c1.to_c();
        let c2 = c2.to_c();
        ffi::action_defausser(c1, c2).to_rust()
    }
}

/// Jouer l'action choisir entre trois cartes
///
/// ### Parameters
///  - `c1`: La première carte à jouer
///  - `c2`: La deuxième carte à jouer
///  - `c3`: La troisième carte à jouer
pub fn action_choix_trois(c1: i32, c2: i32, c3: i32) -> Error {
    unsafe {
        let c1 = c1.to_c();
        let c2 = c2.to_c();
        let c3 = c3.to_c();
        ffi::action_choix_trois(c1, c2, c3).to_rust()
    }
}

/// Jouer l'action choisir entre deux paquets de deux cartes
///
/// ### Parameters
///  - `p1c1`: La première carte du premier paquet à jouer
///  - `p1c2`: La deuxième carte du premier paquet à jouer
///  - `p2c1`: La première carte du deuxième paquet à jouer
///  - `p2c2`: La deuxième carte du deuxième paquet à jouer
pub fn action_choix_paquets(p1c1: i32, p1c2: i32, p2c1: i32, p2c2: i32) -> Error {
    unsafe {
        let p1c1 = p1c1.to_c();
        let p1c2 = p1c2.to_c();
        let p2c1 = p2c1.to_c();
        let p2c2 = p2c2.to_c();
        ffi::action_choix_paquets(p1c1, p1c2, p2c1, p2c2).to_rust()
    }
}

/// Choisir une des trois cartes proposées.
///
/// ### Parameters
///  - `c`: Le numéro de la carte choisi (0, 1 ou 2)
pub fn repondre_choix_trois(c: i32) -> Error {
    unsafe {
        let c = c.to_c();
        ffi::repondre_choix_trois(c).to_rust()
    }
}

/// Choisir un des deux paquets proposés.
///
/// ### Parameters
///  - `p`: Le paquet choisi (0 ou 1)
pub fn repondre_choix_paquets(p: i32) -> Error {
    unsafe {
        let p = p.to_c();
        ffi::repondre_choix_paquets(p).to_rust()
    }
}

/// Affiche le contenu d'une valeur de type action
///
/// ### Parameters
///  - `v`: The value to display
pub fn afficher_action(v: Action) {
    unsafe {
        let v = v.to_c();
        ffi::afficher_action(v).to_rust()
    }
}

/// Affiche le contenu d'une valeur de type error
///
/// ### Parameters
///  - `v`: The value to display
pub fn afficher_error(v: Error) {
    unsafe {
        let v = v.to_c();
        ffi::afficher_error(v).to_rust()
    }
}

/// Affiche le contenu d'une valeur de type joueur
///
/// ### Parameters
///  - `v`: The value to display
pub fn afficher_joueur(v: Joueur) {
    unsafe {
        let v = v.to_c();
        ffi::afficher_joueur(v).to_rust()
    }
}

/// Affiche le contenu d'une valeur de type action_jouee
///
/// ### Parameters
///  - `v`: The value to display
pub fn afficher_action_jouee(v: &ActionJouee) {
    unsafe {
        let v = UnsafeCell::new(v.to_c());
        ffi::afficher_action_jouee(v.get().read()).to_rust()
    }
}
