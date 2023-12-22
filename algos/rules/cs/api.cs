// SPDX-License-Identifier: GPL-2.0-or-later
// Copyright (c) 2012-2020 Association Prologin <association@prologin.org>


using System.Runtime.CompilerServices;

namespace Champion {
    // Les actions de jeu
    public enum Action {
        VALIDER, //< Valide une unique carte
        DEFAUSSER, //< Défausse deux cartes
        CHOIX_TROIS, //< Donne le choix entre trois cartes
        CHOIX_PAQUETS, //< Donne le choix entre deux paquets de deux cartes
        PREMIER_JOUEUR, //< Aucune action n'a été jouée (utilisé dans tour_precedent)
    }

    // Enumeration contentant toutes les erreurs possibles
    public enum Error {
        OK, //< pas d'erreur
        ACTION_DEJA_JOUEE, //< l'action a déjà été jouée
        CARTES_INVALIDES, //< vous ne pouvez pas jouer ces cartes
        PAQUET_INVALIDE, //< ce paquet n'existe pas
        GEISHA_INVALIDES, //< cette Geisha n'existe pas (doit être un entier entre 0 et NB_GEISHA - 1)
        JOUEUR_INVALIDE, //< ce joueur n'existe pas
        CHOIX_INVALIDE, //< vous ne pouvez pas répondre à ce choix
        ACTION_INVALIDE, //< vous ne pouvez pas jouer cette action maintenant
    }

    // Enumeration représentant les différents joueurs
    public enum Joueur {
        JOUEUR_1, //< Le joueur 1
        JOUEUR_2, //< Le joueur 2
        EGALITE, //< Égalité, utilisé uniquement dans possession_geisha
    }

    // La description d'une action jouée
    class ActionJouee {
        public ActionJouee() {}
        public Action Act; //< L'action jouée
        public int C1; //< Si act==VALIDER ou act==DEFAUSSER, -1 sinon la première carte (du premier paquet)
        public int C2; //< Si act==V|D: -1 sinon la deuxième carte (du premier paquet)
        public int C3; //< Si act==V|D: -1 sinon la troisième carte (ou la première carte du second paquet si act==choix paquet)
        public int C4; //< Si act!=choix paquet: -1 sinon la deuxième carte du second paquet
    }

    class Api {

        // Les 7 Geisha (2, 2, 2, 3, 3, 4, 5)
        public const int NB_GEISHA = 7;

        // Le nombre total de cartes (2 + 2 + 2 + 3 + 3 + 4 + 5)
        public const int NB_CARTES_TOTALES = 21;

        // Le nombre de cartes que chaque personne a au début
        public const int NB_CARTES_DEBUT = 6;

        // Le nombre de cartes écartées au début du jeu
        public const int NB_CARTES_ECARTEES = 1;

        // Le nombre total d'actions que chaque joueur devra faire
        public const int NB_ACTIONS = 4;

        // Le nombre total de manches avant la fin de la partie
        public const int NB_MANCHES_MAX = 3;

        // La valeur (et le nombre de cartes) de chaque Geisha séparée par des
        // |
        public const string GEISHA_VALEUR = "2|2|2|3|3|4|5";

        // Renvoie l'identifiant du joueur
        [MethodImplAttribute(MethodImplOptions.InternalCall)]
        public static extern Joueur IdJoueur();

        // Renvoie l'identifiant de l'adversaire
        [MethodImplAttribute(MethodImplOptions.InternalCall)]
        public static extern Joueur IdAdversaire();

        // Renvoie le numéro de la manche (entre 0 et 2)
        [MethodImplAttribute(MethodImplOptions.InternalCall)]
        public static extern int Manche();

        // Renvoie le numéro du tour (entre 0 et 7)
        [MethodImplAttribute(MethodImplOptions.InternalCall)]
        public static extern int Tour();

        // Renvoie l'action jouée par l'adversaire
        [MethodImplAttribute(MethodImplOptions.InternalCall)]
        public static extern ActionJouee TourPrecedent();

        // Renvoie le nombre de cartes validées par le joueur pour la Geisha (la carte
// validée secrètement n'est pas prise en compte)
        [MethodImplAttribute(MethodImplOptions.InternalCall)]
        public static extern int NbCartesValidees(Joueur j, int g);

        // Renvoie qui possède la Geisha
        [MethodImplAttribute(MethodImplOptions.InternalCall)]
        public static extern Joueur PossessionGeisha(int g);

        // Renvoie si l'action a déjà été jouée par le joueur
        [MethodImplAttribute(MethodImplOptions.InternalCall)]
        public static extern bool EstJoueeAction(Joueur j, Action a);

        // Renvoie le nombre de cartes que le joueur a
        [MethodImplAttribute(MethodImplOptions.InternalCall)]
        public static extern int NbCartes(Joueur j);

        // Renvoie les cartes que vous avez
        [MethodImplAttribute(MethodImplOptions.InternalCall)]
        public static extern int[] CartesEnMain();

        // Renvoie la carte que vous avez piochée au début du tour
        [MethodImplAttribute(MethodImplOptions.InternalCall)]
        public static extern int CartePiochee();

        // Jouer l'action valider une carte
        [MethodImplAttribute(MethodImplOptions.InternalCall)]
        public static extern Error ActionValider(int c);

        // Jouer l'action défausser deux cartes
        [MethodImplAttribute(MethodImplOptions.InternalCall)]
        public static extern Error ActionDefausser(int c1, int c2);

        // Jouer l'action choisir entre trois cartes
        [MethodImplAttribute(MethodImplOptions.InternalCall)]
        public static extern Error ActionChoixTrois(int c1, int c2, int c3);

        // Jouer l'action choisir entre deux paquets de deux cartes
        [MethodImplAttribute(MethodImplOptions.InternalCall)]
        public static extern Error ActionChoixPaquets(int p1c1, int p1c2, int p2c1, int p2c2);

        // Choisir une des trois cartes proposées.
        [MethodImplAttribute(MethodImplOptions.InternalCall)]
        public static extern Error RepondreChoixTrois(int c);

        // Choisir un des deux paquets proposés.
        [MethodImplAttribute(MethodImplOptions.InternalCall)]
        public static extern Error RepondreChoixPaquets(int p);

        // Affiche le contenu d'une valeur de type action
        [MethodImplAttribute(MethodImplOptions.InternalCall)]
        public static extern void AfficherAction(Action v);

        // Affiche le contenu d'une valeur de type error
        [MethodImplAttribute(MethodImplOptions.InternalCall)]
        public static extern void AfficherError(Error v);

        // Affiche le contenu d'une valeur de type joueur
        [MethodImplAttribute(MethodImplOptions.InternalCall)]
        public static extern void AfficherJoueur(Joueur v);

        // Affiche le contenu d'une valeur de type action_jouee
        [MethodImplAttribute(MethodImplOptions.InternalCall)]
        public static extern void AfficherActionJouee(ActionJouee v);
    }
}
