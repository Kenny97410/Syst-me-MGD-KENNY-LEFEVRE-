#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MGD (Modèle Génératif Dialectique) v1.2
Code source complet, typé et documenté
Auteur: Kenny Lefevre
Date: 2025-11-09
Licence: CC-BY-NC-4.0

Ce modèle formalise la dialectique (Thèse / Antithèse / Synthèse)
comme un système génératif vectoriel dans ℕ³, soumis à un axiome
d’équilibre : S ≥ T + A.

Opérateurs :
  - Hybridation : combinaison additive de deux états
  - Résolution : correction vers l’équilibre
  - Ancrage : condition d’enchâssement récursif (A₁ = T₂)

Utilisation :
    python mgd.py
"""

from itertools import product
from typing import Tuple, Set, List, Dict, Any, Optional


Vector = Tuple[int, int, int]


class MGDMoteur:
    """
    Moteur du Modèle Génératif Dialectique (MGD).
    Représente les états dialectiques comme des vecteurs (T, A, S).
    """

    def __init__(self) -> None:
        """Initialise les trois états fondamentaux."""
        self.M_THESE: Vector = (1, 0, 0)
        self.M_ANTITHESE: Vector = (0, 1, 0)
        self.M_SYNTHESE: Vector = (0, 0, 1)

    def verifier_axiome(self, t: int, a: int, s: int) -> bool:
        """
        Vérifie l’axiome d’équilibre du modèle :
            S ≥ T + A

        Un état est dit « équilibré » s’il satisfait cet axiome.
        """
        return s >= (t + a)

    def est_equilibre(self, v: Vector) -> bool:
        """Alias plus parlant pour `verifier_axiome`."""
        return self.verifier_axiome(*v)

    def hybridation(self, v1: Vector, v2: Vector) -> Vector:
        """
        Opérateur d’hybridation : combinaison additive des composantes.
        Produit un état de « tension » qui peut être instable.
        """
        return tuple(x + y for x, y in zip(v1, v2))

    def resolution(self, v: Vector) -> Vector:
        """
        Opérateur de résolution : stabilise un état en garantissant
        l’axiome d’équilibre.

        Formule : (T, A, max(S, T + A))
        L’opérateur est idempotent : Σ(Σ(v)) = Σ(v)
        """
        t, a, s = v
        s_equilibre = t + a
        if s >= s_equilibre:
            return v  # déjà équilibré
        return (t, a, s_equilibre)

    def generer_hybridations(self, max_iterations: int = 5, verbose: bool = False) -> Tuple[List[int], Set[Vector]]:
        """
        Génère des états dialectiques par hybridation itérative
        des états connus, suivie de résolution.

        Retourne :
            - historique du nombre de nouveaux états par itération,
            - ensemble de tous les états générés (équilibrés).
        """
        # États de base (déjà équilibrés)
        etats: Set[Vector] = {self.M_THESE, self.M_ANTITHESE, self.M_SYNTHESE}
        historique: List[int] = []

        if verbose:
            print(f"  États initiaux : {len(etats)}")

        for iteration in range(max_iterations):
            nouveaux: Set[Vector] = set()
            liste_etats = list(etats)

            # Génère toutes les paires non orientées (incluant (x,x))
            for i, s1 in enumerate(liste_etats):
                for s2 in liste_etats[i:]:
                    hybrid = self.hybridation(s1, s2)
                    stable = self.resolution(hybrid)
                    if stable not in etats:
                        nouveaux.add(stable)

            if not nouveaux:
                if verbose:
                    print(f"  → Stabilisation atteinte à l’itération {iteration + 1}")
                break

            etats.update(nouveaux)
            historique.append(len(nouveaux))

            if verbose:
                print(f"  Itération {iteration + 1}: "
                      f"{len(nouveaux)} nouveaux états | Total: {len(etats)}")

        return historique, etats

    def generer_cube_27(self) -> List[Vector]:
        """
        Génère l’espace théorique C27 = {0,1,2}³.
        Cet espace inclut des états non équilibrés et sert de cadre
        pour explorer des configurations potentielles (ex. poétiques,
        récursives, ou transitoires).
        """
        return list(product(range(3), repeat=3))

    def ancrage_valide(self, v1: Vector, v2: Vector) -> bool:
        """
        Règle d’ancrage pour l’enchâssement récursif :
            L’antithèse du premier état (v1[1]) doit coïncider
            avec la thèse du second (v2[0]).

        Interprétation : la tension du premier devient la base du second.
        """
        return v1[1] == v2[0]

    def analyser_cube_27(self) -> Dict[str, Any]:
        """
        Analyse statistique du cube C27 :
            - nombre total de points,
            - nombre de paires valides selon la règle d’ancrage,
            - ratio en pourcentage.
        """
        cube = self.generer_cube_27()
        total_paires = len(cube) ** 2
        ancrages_valides = sum(
            1 for p1 in cube for p2 in cube if self.ancrage_valide(p1, p2)
        )
        ratio = (ancrages_valides / total_paires) * 100

        return {
            "nombre_points": len(cube),
            "total_paires": total_paires,
            "ancrages_valides": ancrages_valides,
            "ratio_percentage": round(ratio, 2)
        }

    def generer_triade_poetique(
        self,
        v1: Vector,
        v2: Vector,
        concepts: Optional[Dict[Vector, str]] = None
    ) -> Dict[str, Any]:
        """
        Génère une triade poétique à partir de deux concepts.

        Étapes :
            1. Hybridation → tension
            2. Résolution → synthèse équilibrée
        """
        hybrid = self.hybridation(v1, v2)
        synthese = self.resolution(hybrid)

        label = lambda v: concepts.get(v, str(v)) if concepts else str(v)

        return {
            "concept_1": label(v1),
            "concept_2": label(v2),
            "tension": hybrid,
            "synthese": synthese,
            "equilibre": self.est_equilibre(synthese)
        }


# ============================================================
# DÉMONSTRATION ET TESTS
# ============================================================

if __name__ == "__main__":
    print("=" * 70)
    print("MGD (Modèle Génératif Dialectique) — Démonstration complète")
    print("Auteur: Kenny Lefevre • Licence: CC-BY-NC-4.0")
    print("=" * 70)

    moteur = MGDMoteur()

    # ——————————————————————————————————
    # TEST 1 : Hybridation et résolution
    # ——————————————————————————————————
    print("\n[TEST 1] Hybridation et résolution dialectique")
    print("-" * 70)

    these = moteur.M_THESE
    antithese = moteur.M_ANTITHESE

    print(f"Thèse      : {these}")
    print(f"Antithèse  : {antithese}")

    tension = moteur.hybridation(these, antithese)
    print(f"\nTension    : {these} ⊕ {antithese} = {tension}")
    print(f"Équilibré ? {moteur.est_equilibre(tension)}")

    synthese = moteur.resolution(tension)
    print(f"Synthèse   : Σ({tension}) = {synthese}")
    print(f"Équilibré ? {moteur.est_equilibre(synthese)} ✓")

    # ——————————————————————————————————
    # TEST 2 : Génération itérative
    # ——————————————————————————————————
    print("\n\n[TEST 2] Génération dialectique (5 itérations max)")
    print("-" * 70)

    historique, etats = moteur.generer_hybridations(max_iterations=5, verbose=True)

    print(f"\n→ Résumé de la génération :")
    for i, nb in enumerate(historique, 1):
        print(f"  Itération {i}: {nb} nouveaux états")
    print(f"  Total d’états uniques : {len(etats)}")

    # ——————————————————————————————————
    # TEST 3 : Structure C27
    # ——————————————————————————————————
    print("\n\n[TEST 3] Analyse de l’espace théorique C27")
    print("-" * 70)

    stats = moteur.analyser_cube_27()
    print(f"  Points dans C27          : {stats['nombre_points']}")
    print(f"  Paires d’ancrage valides : {stats['ancrages_valides']} / {stats['total_paires']}")
    print(f"  Ratio d’ancrage          : {stats['ratio_percentage']} %")

    # ——————————————————————————————————
    # TEST 4 : Triade poétique
    # ——————————————————————————————————
    print("\n\n[TEST 4] Triade poétique")
    print("-" * 70)

    concepts = {
        (1, 0, 0): "Interrogation",
        (0, 1, 0): "Négation",
        (0, 0, 1): "Affirmation"
    }

    triade = moteur.generer_triade_poetique(these, antithese, concepts)

    print(f"  Concept 1    : {triade['concept_1']}")
    print(f"  Concept 2    : {triade['concept_2']}")
    print(f"  État tension : {triade['tension']}")
    print(f"  Synthèse     : {triade['synthese']}")
    print(f"  Équilibré ?  : {triade['equilibre']} ✓")

    print("\n" + "=" * 70)
    print("✓ Démonstration terminée avec succès.")
    print("=" * 70)
