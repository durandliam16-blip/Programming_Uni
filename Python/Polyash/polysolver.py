#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Module de résolution du projet Poly#."""

from typing import Dict, List, Tuple

# Constante pour la durée max d'un feu vert
# 6 Car optimal pour les challenges donnés (après tests avec plusieurs autres valeurs)
duree_max = 6
# Constante pour la durée min d'un feu vert
# 1 Car optimal pour les challenges donnés (après tests avec plusieurs autres valeurs)
duree_min = 1


def resolution(challenge: Dict) -> Dict:
    """
    Pour cette solution, nous avons compilé deux idées :
    - "idée1" : on attribue une durée à chaque rue selon un calcul prévisionnel en fonction du nombre de voitures qui vont l'emprunter
    - Amélioration : Pour chaque intersection, on met en premier les rues ou démarrent les voitures

    :param challenge: dictionnaire retourné par parse_challenge
    :return: dictionnaire représentant la solution
    """

    planif = {}
    # Appel la fonction "compt_usage_rues" pour obtenir les nb à use pour calcul
    comptage_usage_rues = compt_usage_rues(challenge)

    # Compter les voitures bloquées au feu à T=0
    # Ce sont les voitures qui sont à leur 1ère rue au lancement du programme.
    voiture_debut = {}
    for descript_voitures in challenge["listeCar"]:
        for voiture in descript_voitures.values():
            premiere_rue = voiture.streetsTraverse[0]
            voiture_debut[premiere_rue] = (
                voiture_debut.get(premiere_rue, 0) + 1
            )  # Compteur des rues de départ

    # Attribution des durées :
    for description_intersection in challenge["listeIntersection"]:
        for intersection_id, intersection in description_intersection.items():
            resultat_planning: List[Tuple[str, int]] = []

            # Appel la fonction "temps_inter" pour faire l'attribution des durées
            # Récupère directement la liste de forme [(rue1, duree x), (rue2, duree y), ...]
            resultat_planning = temps_inter(
                intersection, comptage_usage_rues, voiture_debut
            )

            # Si planning pas vide alors on l'ajoute
            if resultat_planning:
                planif[intersection_id] = resultat_planning

    return {"planif": planif}


def compt_usage_rues(challenge: Dict) -> Dict[str, int]:
    """
    Compte l'utilisation de chaque rue en fonction des trajets des voitures prédefinies.
    """
    utilisation_rues = {}
    for descript_voitures in challenge["listeCar"]:
        for voiture in descript_voitures.values():
            # Ignore l'id de la voiture car pas besoin pour compter
            for rue in voiture.streetsTraverse[:-1]:
                # On ignore la dernière rue car c'est l'arrivée
                utilisation_rues[rue] = utilisation_rues.get(rue, 0) + 1
                # Permet de mettre 0 si trouve pas la rue
                # +1 car compteur cad augmente le nb actuel
    return utilisation_rues


def temps_inter(
    inter: Dict, usage_rue: Dict[str, int], voiture_depart: Dict[str, int]
) -> List[Tuple[str, int]]:
    """
    Analyse des rue les plus utilisées pour adapter les temps de feu :
    A- compteur de voiture pour chaque rues en lisant les trajets
    B- pour chaque inter, comparer rues entrantes par division cad pour rue 1 faire score=(val_rue/val_somme_total)
    C- adapter temps en fonction du score (prendre en compte temps simu), ex si une rue prend ⅔ (c’est le score) des voitures alors prend ⅔ des seconde de simu puis 2ème transfo : divise par nb de rues de l’inter (ou ça *2 à voir) + adapter flottants
    """

    # S'assure de pas donner de temps aux rues vides
    rues_actives = []
    for rue in inter.incoming_roads:
        # On verif si la rue est dans notre dico de comptage
        if usage_rue.get(rue.name, 0) > 0:
            rues_actives.append(rue)
    if not rues_actives:
        return []

    # Tri qui ordonne les rues de l'intersection en fonction des rues étant le départ de voitures
    # Plus une rue est le départ de voitures, plus elle est prioritaire
    # En cas d'égalité, on utilise l'usage global de la rue
    rues_actives.sort(
        key=lambda r: (voiture_depart.get(r.name, 0), usage_rue.get(r.name, 0)),
        reverse=True,
    )

    # Calcul du trafic total de cette intersection
    trafic_total_inter = sum(usage_rue[r.name] for r in rues_actives)
    nb_rues = len(rues_actives)  # nb de rues totales

    planning = []
    for rue in rues_actives:
        nb_voitures = usage_rue[rue.name]

        # On calcule la moyenne de trafic par rue sur cette intersection
        moyenne_trafic = trafic_total_inter / nb_rues

        # On calcule la durée proportionnellement à cette moyenne
        # Si une rue a exactement la moyenne, elle aura 1s ou 2s, si elle a 3x plus que la moyenne, elle aura plus, etc.
        duree = round(nb_voitures / moyenne_trafic)

        # Cap de la durée pour pas avoir des feux verts trop longs
        # Conastante magique duree_max = 6 Car optimal pour les challenges donnés (après tests avec plusieurs autres valeurs)
        if duree > duree_max:
            duree = duree_max
        # On s'assure que la durée est au moins de 1 seconde
        if duree < duree_min:
            duree = duree_min

        planning.append((rue.name, duree))
    return planning


def sauvegarde_solution(filename: str, solution: Dict) -> None:
    """
    Sauvegarde la solution dans un fichier texte au format Hash Code :

    Ligne 1 : A = nombre d'intersections avec un programme de feux.
    Puis pour chaque intersection :
    - une ligne : id_intersection
    - une ligne : E_i = nb de rues entrantes gérées
    - E_i lignes : "<nom_de_rue> <durée>"

    :param filename: chemin du fichier de sortie
    :param solution: dictionnaire produit par solve()qq
    """
    planif: Dict[int, List[Tuple[str, int]]] = solution["planif"]

    with open(filename, "w") as f:
        f.write(str(len(planif)) + "\n")

        # Retranscrit le planning des rues en texte :
        for inter_id in sorted(planif.keys()):
            inter_planif = planif[inter_id]
            f.write(str(inter_id) + "\n")
            f.write(str(len(inter_planif)) + "\n")
            for street_nom, duree in inter_planif:
                f.write(f"{street_nom} {duree}\n")


def simulation_traffic(challenge: Dict, solution: Dict) -> List[Dict[int, int]]:
    """
    Simule le trafic et retourne la liste finishers.
    finishers = [{id_voiture: D - T}, ...] pour chaque voiture arrivée à temps.

    :param challenge: le  challenge actuel
    :param solution: dictionnaire produit par solve()
    """

    info = challenge["informationGeneralesSimulation"]
    D = info.duree

    planifs: Dict[int, List[Tuple[str, int]]] = solution["planif"]

    # Rues par nom
    rues_par_nom = {}
    for e in challenge["listeStreet"]:
        for nom, rue in e.items():
            rues_par_nom[nom] = rue

    # Chemins des voitures
    chemins_voiture: Dict[int, List[str]] = {}
    for e in challenge["listeCar"]:
        for id_voiture, voiture in e.items():
            chemins_voiture[int(id_voiture)] = voiture.streetsTraverse

    # Files d'attente par rue entrante
    files: Dict[str, List[Tuple[int, int]]] = {}
    # on stocke (id_voiture, idx) où idx = index de la rue actuelle dans le trajet

    # Arrivées planifiées
    # arrivals[t] = liste de (id_voiture, street_name, idx)
    arrivees: Dict[int, List[Tuple[int, str, int]]] = {}

    # Préparer cycle des feux
    cycles = {}  # inter_id -> (planif, longueur_totale)
    for inter_id, planif in planifs.items():
        longueur_totale = sum(dur for _, dur in planif)
        if longueur_totale > 0:
            cycles[inter_id] = (planif, longueur_totale)

    # Initialiser : chaque voiture démarre sur sa 1ère rue à t=0
    for id_voiture, chemin in chemins_voiture.items():
        if not chemin:
            continue
        premiere_rue = chemin[0]
        t_arrive = rues_par_nom[premiere_rue].size
        if t_arrive <= D:
            arrivees.setdefault(t_arrive, []).append((id_voiture, premiere_rue, 0))

    # Voitures arrivées à temps
    finishers: List[Dict[int, int]] = []

    # Simulation seconde par seconde
    for t in range(D + 1):
        # 1) gérer les arrivées à t
        if t in arrivees:
            for id_voiture, nom_rue, idx in arrivees[t]:
                path = chemins_voiture[id_voiture]
                # Si c'est la dernière rue -> fin
                if idx == len(path) - 1:
                    finishers.append({id_voiture: D - t})  # D - T (temps restant)
                else:
                    # sinon la voiture attend au feu à la fin de nom_rue
                    files.setdefault(nom_rue, []).append((id_voiture, idx))

        # 2) faire passer les voitures aux intersections (1 voiture max / intersection / seconde)
        for inter_id, (planif, longueur_totale) in cycles.items():
            # calcul de la rue verte à l'instant t
            x = t % longueur_totale
            feu_vert = None
            acc = 0
            for sname, dur in planif:
                acc += dur
                if x < acc:
                    feu_vert = sname
                    break

            if feu_vert is None:
                continue

            q = files.get(feu_vert, [])
            if q:
                id_voiture, idx = q.pop(0)

                chemin = chemins_voiture[id_voiture]
                next_street = chemin[idx + 1]

                # la voiture roule sur next_street et arrivera plus tard
                t_arrive = t + rues_par_nom[next_street].size
                if t_arrive <= D:
                    arrivees.setdefault(t_arrive, []).append(
                        (id_voiture, next_street, idx + 1)
                    )

    return finishers


def score_solution(challenge: Dict, solution: Dict) -> int:
    """
    Score : F + (D - T) pour les voitures arrivées avant le temps limite
    """

    award_par_arrivee = challenge["informationGeneralesSimulation"].points
    finishers = simulation_traffic(challenge, solution)
    total = 0
    nb_finishers = len(finishers)

    # Calcul points par voitures arrivées
    for i in range(nb_finishers):
        for _, value in finishers[i].items():
            total += award_par_arrivee + value
    return total
