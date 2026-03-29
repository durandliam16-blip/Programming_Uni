def add (commande:str)->int:
    pass

def q1 (commande:str)->int:
    if commande == "":
        return 0
    vars = commande.split(",")
    total = 0
    for var in vars:
        total += int(var)
    return total

def q2 (commande:str)->int:
    if commande == "":
        return 0
    vars = commande.split(",")
    total = 0
    for var in vars:
        total += int(var)
    return total

def q3(commande: str) -> int:
    if commande == "":
        return 0
    #Verif pas deux séparateurs consécutifs
    if ",\n" in commande or "\n," in commande:
        return None
    commande_normale = commande.replace("\n", ",")
    result = q2(commande_normale)
    return result

def q4(commande: str) -> int:
    if commande == "":
        return 0
    #Verif pas deux séparateurs consécutifs
    if "//" == commande[0:1]:
        if ",\n" in commande or "\n," in commande:
            return None
        commande_normale = commande.replace("\n", ",")
        commande_normale = commande.replace("//",commande[2], ",")
        result = q2(commande_normale)
        return result
    if ",\n" in commande or "\n," in commande:
        return None
    commande_normale = commande.replace("\n", ",")
    result = q2(commande_normale)
    return result

if __name__ == "__main__":
    print(q1("")) 