{-# LANGUAGE ForeignFunctionInterface #-}

-- This file was generated by stechec2-generator. DO NOT EDIT.

module Champion where

import Api


-- Fonction appelée au début du jeu
init_jeu :: IO ()
init_jeu = return () -- TODO

-- Fonction appelée au début du tour
jouer_tour :: IO ()
jouer_tour = return () -- TODO

-- Fonction appelée lors du choix entre les trois cartes lors de l'action de
-- l'adversaire (cf tour_precedent)
repondre_action_choix_trois :: IO ()
repondre_action_choix_trois = return () -- TODO

-- Fonction appelée lors du choix entre deux paquet lors de l'action de
-- l'adversaire (cf tour_precedent)
repondre_action_choix_paquets :: IO ()
repondre_action_choix_paquets = return () -- TODO

-- Fonction appelée à la fin du jeu
fin_jeu :: IO ()
fin_jeu = return () -- TODO


hs_init_jeu = init_jeu
foreign export ccall hs_init_jeu :: IO ()

hs_jouer_tour = jouer_tour
foreign export ccall hs_jouer_tour :: IO ()

hs_repondre_action_choix_trois = repondre_action_choix_trois
foreign export ccall hs_repondre_action_choix_trois :: IO ()

hs_repondre_action_choix_paquets = repondre_action_choix_paquets
foreign export ccall hs_repondre_action_choix_paquets :: IO ()

hs_fin_jeu = fin_jeu
foreign export ccall hs_fin_jeu :: IO ()
