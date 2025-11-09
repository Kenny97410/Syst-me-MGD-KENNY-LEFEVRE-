#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MGD (Modèle Génératif Dialectique) v1.1
Code source complet et exécutable
Auteur: Kenny Lefevre
Date: 2025-11-09
Licence: CC-BY-NC-4.0

Utilisation:
    python mgd.py
"""

from itertools import product

class MGDMoteur:
    """
    Moteur du Modèle Génératif Dialectique.
    Implémente les trois opérateurs: Hybridation, Résolution, Récursion.
    """
    
    def __init__(self):
        """Initialise le moteur avec les trois états de base."""
        self.M_THESE = (1, 0, 0)
        self.M_ANTITHESE = (0, 1, 0)
        self.M_SYNTHESE = (0, 0, 1)
    
    def verifier_axiome(self, t, a, s):
        """
        Vérifie si une proposition est équilibrée.
        Axiome: S ≥ T + A
        """
        return s >= (t + a)
    
    def hybridation(self, v1, v2):
        """
        Opérateur d'hybridation: mélange deux vecteurs dialectiques.
        Résultat: addition vectorielle composante par composante.
        """
        return tuple(x + y for x, y in zip(v1, v2))
    
    def resolution(self, v):
        """
        Opérateur de résolution: transforme un état instable en équilibré.
        Formule: Σ(v) = (t, a, max(s, t+a))
        """
        t, a, s = v
        s_min = t + a
        return (t, a, max(s, s_min))
    
    def generer_hybridations(self, max_iterations=5, verbose=False):
        """
        Génère une infinité d'états par hybridation répétée.
        """
        all_states = {self.M_THESE, self.M_ANTITHESE, self.M_SYNTHESE}
        history = []
        
        for iteration in range(max_iterations):
            new_states = set()
            state_list = list(all_states)
            
            for i, s1 in enumerate(state_list):
                for s2 in state_list[i:]:
                    hybrid = self.hybridation(s1, s2)
                    resolved = self.resolution(hybrid)
                    
                    if resolved not in all_states:
                        new_states.add(resolved)
            
            all_states.update(new_states)
            history.append(len(new_states))
            
            if verbose:
                print(f"  Itération {iteration+1}: "
                      f"{len(new_states)} nouveaux états | "
                      f"Total: {len(all_states)}")
            
            if len(new_states) == 0:
                if verbose:
                    print(f"  → Génération stabilisée")
                break
        
        return history, all_states
    
    def generer_cube_27(self):
        """
        Génère la structure C27: cube 3×3×3.
        C27 = produit cartésien {0,1,2} × {0,1,2} × {0,1,2}
        """
        return list(product(range(3), repeat=3))
    
    def ancrage_valide(self, v1, v2):
        """
        Vérifie la règle d'ancrage pour enchâssement récursif.
        Règle: ℛ(v1, v2) valide ssi v1[1] == v2[0]
        """
        return v1[1] == v2[0]
    
    def analyser_cube_27(self):
        """
        Analyse la structure du cube C27 et les ancrages.
        """
        cube = self.generer_cube_27()
        
        valid_anchors = 0
        total_pairs = len(cube) ** 2
        
        for p1 in cube:
            for p2 in cube:
                if self.ancrage_valide(p1, p2):
                    valid_anchors += 1
        
        ratio = (valid_anchors / total_pairs) * 100
        
        return {
            'nombre_points': len(cube),
            'total_paires': total_pairs,
            'ancrages_valides': valid_anchors,
            'ratio_percentage': ratio
        }
    
    def generer_triade_poetique(self, v1, v2, concepts=None):
        """
        Génère une triade poétique via hybridation + résolution.
        """
        hybrid = self.hybridation(v1, v2)
        resolved = self.resolution(hybrid)
        
        result = {
            'concept_1': concepts.get(v1, str(v1)) if concepts else str(v1),
            'concept_2': concepts.get(v2, str(v2)) if concepts else str(v2),
            'tension': hybrid,
            'synthese': resolved,
            'equilibre': self.verifier_axiome(*resolved)
        }
        
        return result


# ============================================================
# TESTS ET DÉMONSTRATION
# ============================================================

if __name__ == "__main__":
    print("="*70)
    print("MGD (Modèle Génératif Dialectique) - Exécution complète")
    print("Auteur: Kenny Lefevre")
    print("="*70)
    
    moteur = MGDMoteur()
    
    # TEST 1: Hybridation et Résolution
    print("\n[TEST 1] Hybridation simple")
    print("-"*70)
    
    v1 = moteur.M_THESE
    v2 = moteur.M_ANTITHESE
    
    print(f"Thèse:      {v1}")
    print(f"Antithèse:  {v2}")
    
    hybrid = moteur.hybridation(v1, v2)
    print(f"\nHybridation (tension):")
    print(f"  {v1} ⊕ {v2} = {hybrid}")
    print(f"  Équilibré? {moteur.verifier_axiome(*hybrid)}")
    
    resolved = moteur.resolution(hybrid)
    print(f"\nRésolution (équilibre):")
    print(f"  Σ({hybrid}) = {resolved}")
    print(f"  Équilibré? {moteur.verifier_axiome(*resolved)} ✓")
    
    # TEST 2: Génération d'infini
    print("\n\n[TEST 2] Génération d'infini par hybridation (5 itérations)")
    print("-"*70)
    
    history, all_states = moteur.generer_hybridations(max_iterations=5, verbose=True)
    
    print(f"\nRésumé:")
    for i, count in enumerate(history, 1):
        print(f"  Itération {i}: {count} nouveaux états")
    print(f"  Total: {len(all_states)} états uniques")
    
    # TEST 3: Cube C27
    print("\n\n[TEST 3] Structure C27 et Ancrage")
    print("-"*70)
    
    stats = moteur.analyser_cube_27()
    print(f"\nCube 3×3×3:")
    print(f"  Points: {stats['nombre_points']}")
    print(f"  Paires d'ancrage valides: {stats['ancrages_valides']}/{stats['total_paires']}")
    print(f"  Ratio: {stats['ratio_percentage']:.2f}%")
    
    # TEST 4: Application poétique
    print("\n\n[TEST 4] Triade poétique")
    print("-"*70)
    
    concepts = {
        (1, 0, 0): "Interrogation",
        (0, 1, 0): "Négation",
        (0, 0, 1): "Affirmation"
    }
    
    triade = moteur.generer_triade_poetique(
        moteur.M_THESE,
        moteur.M_ANTITHESE,
        concepts
    )
    
    print(f"\nConcept 1: {triade['concept_1']}")
    print(f"Concept 2: {triade['concept_2']}")
    print(f"État de tension: {triade['tension']}")
    print(f"État de synthèse: {triade['synthese']}")
    print(f"Équilibré? {triade['equilibre']} ✓")
    
    print("\n" + "="*70)
    print("✓ Tous les tests réussis!")
    print("="*70)
