Point = tuple[int, int] # alias de type
def intersect(O: Point, A: Point, B: Point) -> bool:
    (xO, yO), (xA, yA), (xB, yB) = O, A, B
    return (
        (yO <= yA) == (yO > yB) and # ordonn´ee dans l'intervalle
        xO < (xB - xA) * (yO - yA) / (yB - yA) + xA # point du bon c^ot´e
    )
