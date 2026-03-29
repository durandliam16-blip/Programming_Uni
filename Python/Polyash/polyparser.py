#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Module de parsing des fichiers d'entrée pour la mise en oeuvre du projet Poly#."""

import re
from Entity.InfoChallenge import InfoChallenge
from Entity.Street import Street
from Entity.Car import Car
from Entity.Intersection import Intersection
from affichage import afficher_challenge


def parse_challenge(filename: str) -> object:
    """Lit un fichier de challenge et extrait les informations nécessaires.
    Vous pouvez choisir la structure de données structurées qui va
    représenter votre challenge: dictionnaire, objet, etc
    """

    with open(filename, "r") as f:
        listeStreet = []
        listeIntersection = []
        listeCar = []

        # Lire la première ligne, la découper, et convertir les valeurs en entier
        firstLine = re.sub(r"\s*#.*", "", f.readline().strip())
        values = firstLine.split()
        nbStreet = int(values[2])
        informationGenerales = InfoChallenge(
            duree=int(values[0]),
            nbIntersection=int(values[1]),
            nbStreet=nbStreet,
            nbVoiture=int(values[3]),
            points=int(values[4]),
        )

        # On lit les autres lignes
        for line in f:
            values = line.split()
            if len(listeStreet) < nbStreet:
                firstIntersection = int(values[0])
                endIntersection = int(values[1])
                name = values[2]
                descriptionStreet = {
                    name: Street(
                        name=name,
                        size=int(values[3]),
                        firstIntersection=firstIntersection,
                        endIntersection=endIntersection,
                    )
                }
                # Si firstIntersection n'est pas présente dans la liste des intersections, on l'ajoute
                if not any(
                    firstIntersection in inter.keys() for inter in listeIntersection
                ):
                    intersection = Intersection(id=firstIntersection)
                    descriptionIntersection = {firstIntersection: intersection}
                    listeIntersection.append(descriptionIntersection)
                else:
                    # On récupère l'intersection existante
                    for inter in listeIntersection:
                        if firstIntersection in inter.keys():
                            intersection = inter[firstIntersection]
                            break
                # On ajoute la rue sortante à l'intersection
                intersection.add_outgoing_road(descriptionStreet[name])

                # Si endIntersection n'est pas présente dans la liste des intersections, on l'ajoute
                if not any(
                    endIntersection in inter.keys() for inter in listeIntersection
                ):
                    intersection = Intersection(id=endIntersection)
                    descriptionIntersection = {endIntersection: intersection}
                    listeIntersection.append(descriptionIntersection)
                else:
                    # On récupère l'intersection existante
                    for inter in listeIntersection:
                        if endIntersection in inter.keys():
                            intersection = inter[endIntersection]
                            break
                # On ajoute la rue entrante à l'intersection
                intersection.add_incoming_road(descriptionStreet[name])
                listeStreet.append(descriptionStreet)

            else:
                carId = str(len(listeCar) + 1)
                car = Car(carId)
                car.addManyStreet(values[1:])
                descriptionCar = {carId: car}
                listeCar.append(descriptionCar)

    challenge = {
        "informationGeneralesSimulation": informationGenerales,
        "listeStreet": listeStreet,
        "listeIntersection": listeIntersection,
        "listeCar": listeCar,
    }

    return challenge


if __name__ == "__main__":
    ch = parse_challenge("challenges/a_example.in")
    afficher_challenge(ch)
