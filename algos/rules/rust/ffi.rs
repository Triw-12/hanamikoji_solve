// SPDX-License-Identifier: GPL-2.0-or-later
// Copyright (c) 2012-2020 Association Prologin <association@prologin.org>

//! Types and conversions for the C interface
//!
//! Please use the tools defined in `api.rs` to interact with the API for
//! hanamikoji.

#![allow(clippy::unit_arg)]
#![allow(clippy::unused_unit)]

use crate::api;

use std::borrow::Borrow;
use std::ffi::{CStr, CString};
use std::{mem::{drop, size_of}, ptr, slice};
use std::os::raw::{c_char, c_double, c_int, c_void};

#[allow(non_camel_case_types)]
pub type c_bool = bool;

/// Stechec2-specific array type.
#[repr(C)]
pub struct Array<T> {
    ptr: *mut T,
    len: usize,
}

impl<T> Drop for Array<T> {
    fn drop(&mut self) {
        unsafe {
            slice::from_raw_parts_mut(self.ptr, self.len)
                .iter_mut()
                .for_each(drop);
            free(self.ptr as _);
        }
    }
}

/// Represents an owned C string that was created by a foreign function using
/// malloc. This means that this string must be deallocated using free.
#[repr(C)]
pub struct RawString {
    ptr: *mut c_char
}

impl Drop for RawString {
    fn drop(&mut self) {
        unsafe {
            free(self.ptr as _);
        }
    }
}

// Enums

#[repr(C)]
#[derive(Clone, Copy)]
pub enum Action {
    Valider,
    Defausser,
    ChoixTrois,
    ChoixPaquets,
    PremierJoueur,
}

#[repr(C)]
#[derive(Clone, Copy)]
pub enum Error {
    Ok,
    ActionDejaJouee,
    CartesInvalides,
    PaquetInvalide,
    GeishaInvalides,
    JoueurInvalide,
    ChoixInvalide,
    ActionInvalide,
}

#[repr(C)]
#[derive(Clone, Copy)]
pub enum Joueur {
    Joueur1,
    Joueur2,
    Egalite,
}

// Structures

#[repr(C)]
pub struct ActionJouee {
    act: Action,
    c1: c_int,
    c2: c_int,
    c3: c_int,
    c4: c_int,
}

// Conversion traits

pub trait CToRust<T> {
    /// Convert from a C-compatible type.
    ///
    /// As there can't be a clear ownership through the ffi, you need to make
    /// sure that foreign code assumes that you will drop provided values.
    unsafe fn to_rust(self) -> T;
}

pub trait RustToC<T> {
    /// Convert to a C-compatible type.
    ///
    /// As there can't be a clear ownership through the ffi, you need to make
    /// sure that foreign code assumes that you will drop provided values.
    unsafe fn to_c(&self) -> T;
}

// Conversions for bool

impl CToRust<bool> for c_bool {
    unsafe fn to_rust(self) -> bool {
        self
    }
}

impl RustToC<c_bool> for bool {
    unsafe fn to_c(&self) -> c_bool {
        *self
    }
}

// Conversions for double

impl CToRust<f64> for c_double {
    unsafe fn to_rust(self) -> f64 {
        self
    }
}

impl RustToC<c_double> for f64 {
    unsafe fn to_c(&self) -> c_double {
        *self
    }
}

// Conversions for int

impl CToRust<i32> for c_int {
    unsafe fn to_rust(self) -> i32 {
        self
    }
}

impl RustToC<c_int> for i32 {
    unsafe fn to_c(&self) -> c_int {
        *self
    }
}

// Conversions for void

impl CToRust<()> for () {
    unsafe fn to_rust(self) -> () {
        self
    }
}

impl RustToC<()> for () {
    unsafe fn to_c(&self) -> () {
        *self
    }
}

// Conversions for string

impl CToRust<String> for RawString {
    unsafe fn to_rust(self) -> String {
        CStr::from_ptr(self.ptr)
            .to_owned()
            .into_string()
            .expect("API provided invalid UTF-8")
    }
}

impl<S> RustToC<RawString> for S
where
    S: AsRef<str>,
{
    unsafe fn to_c(&self) -> RawString {
        let c_string = CString::new(self.as_ref().to_string())
            .expect("string provided to the API contains a null character");
        let len = c_string.as_bytes_with_nul().len();

        let ptr = malloc(len * size_of::<c_char>()) as *mut c_char;
        c_string.as_c_str().as_ptr().copy_to(ptr, len);
        RawString { ptr }
    }
}

// Conversions for array

pub unsafe fn array_of_borrow_to_c<T, U, V>(data: &[T]) -> Array<V>
where
    T: Borrow<U>,
    U: RustToC<V>,
{
    let ptr = malloc(data.len() * size_of::<V>()) as *mut V;

    for (i, item) in data.iter().enumerate() {
        ptr::write(ptr.add(i), item.borrow().to_c());
    }

    Array { ptr, len: data.len() }
}

impl<T, U> CToRust<Vec<U>> for Array<T>
where
    T: CToRust<U>,
{
    unsafe fn to_rust(self) -> Vec<U> {
        (0..self.len)
            .map(|i| self.ptr.add(i).read())
            .map(|item| item.to_rust())
            .collect()
    }
}

impl<T, U> RustToC<Array<U>> for [T]
where
    T: RustToC<U>,
{
    unsafe fn to_c(&self) -> Array<U> {
        array_of_borrow_to_c(self)
    }
}

impl<T, U> RustToC<Array<U>> for Vec<T>
where
    T: RustToC<U>,
{
    unsafe fn to_c(&self) -> Array<U> {
        self[..].to_c()
    }
}

// Conversions for action

impl CToRust<api::Action> for Action {
    unsafe fn to_rust(self) -> api::Action {
        match self {
            Action::Valider => api::Action::Valider,
            Action::Defausser => api::Action::Defausser,
            Action::ChoixTrois => api::Action::ChoixTrois,
            Action::ChoixPaquets => api::Action::ChoixPaquets,
            Action::PremierJoueur => api::Action::PremierJoueur,
        }
    }
}

impl RustToC<Action> for api::Action {
    unsafe fn to_c(&self) -> Action {
        match self {
            api::Action::Valider => Action::Valider,
            api::Action::Defausser => Action::Defausser,
            api::Action::ChoixTrois => Action::ChoixTrois,
            api::Action::ChoixPaquets => Action::ChoixPaquets,
            api::Action::PremierJoueur => Action::PremierJoueur,
        }
    }
}

// Conversions for error

impl CToRust<api::Error> for Error {
    unsafe fn to_rust(self) -> api::Error {
        match self {
            Error::Ok => api::Error::Ok,
            Error::ActionDejaJouee => api::Error::ActionDejaJouee,
            Error::CartesInvalides => api::Error::CartesInvalides,
            Error::PaquetInvalide => api::Error::PaquetInvalide,
            Error::GeishaInvalides => api::Error::GeishaInvalides,
            Error::JoueurInvalide => api::Error::JoueurInvalide,
            Error::ChoixInvalide => api::Error::ChoixInvalide,
            Error::ActionInvalide => api::Error::ActionInvalide,
        }
    }
}

impl RustToC<Error> for api::Error {
    unsafe fn to_c(&self) -> Error {
        match self {
            api::Error::Ok => Error::Ok,
            api::Error::ActionDejaJouee => Error::ActionDejaJouee,
            api::Error::CartesInvalides => Error::CartesInvalides,
            api::Error::PaquetInvalide => Error::PaquetInvalide,
            api::Error::GeishaInvalides => Error::GeishaInvalides,
            api::Error::JoueurInvalide => Error::JoueurInvalide,
            api::Error::ChoixInvalide => Error::ChoixInvalide,
            api::Error::ActionInvalide => Error::ActionInvalide,
        }
    }
}

// Conversions for joueur

impl CToRust<api::Joueur> for Joueur {
    unsafe fn to_rust(self) -> api::Joueur {
        match self {
            Joueur::Joueur1 => api::Joueur::Joueur1,
            Joueur::Joueur2 => api::Joueur::Joueur2,
            Joueur::Egalite => api::Joueur::Egalite,
        }
    }
}

impl RustToC<Joueur> for api::Joueur {
    unsafe fn to_c(&self) -> Joueur {
        match self {
            api::Joueur::Joueur1 => Joueur::Joueur1,
            api::Joueur::Joueur2 => Joueur::Joueur2,
            api::Joueur::Egalite => Joueur::Egalite,
        }
    }
}

// Conversions for action_jouee

impl CToRust<api::ActionJouee> for ActionJouee {
    unsafe fn to_rust(self) -> api::ActionJouee {
        api::ActionJouee {
            act: self.act.to_rust(),
            c1: self.c1.to_rust(),
            c2: self.c2.to_rust(),
            c3: self.c3.to_rust(),
            c4: self.c4.to_rust(),
        }
    }
}

impl RustToC<ActionJouee> for api::ActionJouee {
    unsafe fn to_c(&self) -> ActionJouee {
        ActionJouee {
            act: self.act.to_c(),
            c1: self.c1.to_c(),
            c2: self.c2.to_c(),
            c3: self.c3.to_c(),
            c4: self.c4.to_c(),
        }
    }
}


// Import API functions

extern {
    fn free(ptr: *mut c_void);
    fn malloc(size: usize) -> *mut c_void;

    pub fn id_joueur() -> Joueur;
    pub fn id_adversaire() -> Joueur;
    pub fn manche() -> c_int;
    pub fn tour() -> c_int;
    pub fn tour_precedent() -> ActionJouee;
    pub fn nb_carte_validee(j: Joueur, g: c_int) -> c_int;
    pub fn possession_geisha(g: c_int) -> Joueur;
    pub fn est_jouee_action(j: Joueur, a: Action) -> c_bool;
    pub fn nb_cartes(j: Joueur) -> c_int;
    pub fn cartes_en_main() -> Array<c_int>;
    pub fn carte_pioche() -> c_int;
    pub fn action_valider(c: c_int) -> Error;
    pub fn action_defausser(c1: c_int, c2: c_int) -> Error;
    pub fn action_choix_trois(c1: c_int, c2: c_int, c3: c_int) -> Error;
    pub fn action_choix_paquets(p1c1: c_int, p1c2: c_int, p2c1: c_int, p2c2: c_int) -> Error;
    pub fn repondre_choix_trois(c: c_int) -> Error;
    pub fn repondre_choix_paquets(p: c_int) -> Error;
    pub fn afficher_action(v: Action);
    pub fn afficher_error(v: Error);
    pub fn afficher_joueur(v: Joueur);
    pub fn afficher_action_jouee(v: ActionJouee);
}

// Export user functions

#[no_mangle]
unsafe extern "C" fn init_jeu() {
    crate::init_jeu().to_c()
}

#[no_mangle]
unsafe extern "C" fn jouer_tour() {
    crate::jouer_tour().to_c()
}

#[no_mangle]
unsafe extern "C" fn repondre_action_choix_trois() {
    crate::repondre_action_choix_trois().to_c()
}

#[no_mangle]
unsafe extern "C" fn repondre_action_choix_paquets() {
    crate::repondre_action_choix_paquets().to_c()
}

#[no_mangle]
unsafe extern "C" fn fin_jeu() {
    crate::fin_jeu().to_c()
}
