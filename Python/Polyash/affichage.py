# Fonction d'affichage des différents dictionnaires de Challenge
def afficher_challenge(challenge):
    info = challenge["informationGeneralesSimulation"]
    print("=== Informations générales ===")
    print(
        f"Durée: {info.duree}, Intersections: {info.nbIntersection}, "
        f"Rues: {info.nbStreet}, Voitures: {info.nbVoiture}, Points: {info.points}"
    )

    print("\n=== Rues ===")
    for descriptionStreet in challenge["listeStreet"]:
        for street in descriptionStreet.values():
            print(
                f"- {street.name} (Longueur {street.size}) : Intersection {street.firstIntersection} -> Intersection {street.endIntersection}, Feu: {street.trafficLightColor}"
            )

    print("\n=== Intersections ===")
    for descriptionIntersection in challenge["listeIntersection"]:
        for intersection in descriptionIntersection.values():
            print(f"Intersection {intersection.id}:")
            print(
                f"Routes arrivantes : {[road.name for road in intersection.incoming_roads]}"
            )
            print(
                f"Routes sortantes : {[road.name for road in intersection.outgoing_roads]}"
            )

    print("\n=== Voitures ===")
    for descriptionCar in challenge["listeCar"]:
        for car in descriptionCar.values():
            print(f"Voiture {car.id}:")
            print(f"Parcours : {car.streetsTraverse}")
