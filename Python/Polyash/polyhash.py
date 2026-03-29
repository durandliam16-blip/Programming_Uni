#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Module principal pour la mise en oeuvre du projet Poly#."""

# Vous pouvez structurer votre code en modules pour améliorer la
# compréhension et faciliter le travail collaboratif
from polyparser import parse_challenge
from polysolver import resolution, score_solution, sauvegarde_solution

if __name__ == "__main__":
    # La syntaxe exigée pour appeler le programme est
    # polyhash.py chemin/fichier_entree.txt chemin/fichier_sortie.txt

    # On fournit ici un exemple permettant de passer en paramètre le
    # fichier du challenge et le fichier de sortie. N'hésitez pas si
    # besoin à compléter avec d'autres paramètres/options - en
    # conservant la possibilité de l'appel ci-dessus - en consultant
    # la documentation du module argparse:
    # https://docs.python.org/3/library/argparse.html

    import argparse
    import time
    import os
    from pathlib import Path

    debut_solution = time.time()
    parser = argparse.ArgumentParser(description="Solve Poly# challenge.")
    parser.add_argument(
        "challenge",
        type=str,
        help="challenge definition filename",
        metavar="challenge.txt",
    )
    parser.add_argument(
        "output",
        type=str,
        nargs="?",
        default=None,
        help="output filename (optional)",
        metavar="sortie.txt",
    )
    args = parser.parse_args()

    challenge = parse_challenge(args.challenge)
    solution = resolution(challenge)
    if args.output is not None:
        out_path = Path(args.output)

        #On sauvegarde dans le dossier 'sortie' si aucun répertoire n'est spécifié
        if out_path.parent == Path("") or str(out_path.parent) == ".":
            out_path = Path("sortie") / out_path.name

        #Création du répertoire si nécessaire
        if not out_path.parent.exists():
            out_path.parent.mkdir(parents=True, exist_ok=True)

        sauvegarde_solution(str(out_path), solution)
        print(f"Solution sauvegardée dans {out_path}")
    fin_solution = time.time()
    print(f"Score: {score_solution(challenge, solution)}")
    fin_score = time.time()
    print(f"Temps du calcul du score: {fin_score - fin_solution} secondes")
    print(f"Temps de la solution: {fin_solution - debut_solution} secondes")
