// Include standard library in documentation: `cargo doc --open`
#[doc(inline)]
pub use std;

mod ffi;
pub mod api;

use api::*;


/// Fonction appelée au début du jeu
pub fn init_jeu()
{
    // TODO
}

/// Fonction appelée au début du tour
pub fn jouer_tour()
{
    // TODO
}

/// Fonction appelée lors du choix entre les trois cartes lors de l'action de
/// l'adversaire (cf tour_precedent)
pub fn repondre_action_choix_trois()
{
    // TODO
}

/// Fonction appelée lors du choix entre deux paquet lors de l'action de
/// l'adversaire (cf tour_precedent)
pub fn repondre_action_choix_paquets()
{
    // TODO
}

/// Fonction appelée à la fin du jeu
pub fn fin_jeu()
{
    // TODO
}
