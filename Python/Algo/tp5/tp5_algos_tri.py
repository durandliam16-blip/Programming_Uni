import random
import time

##Ex1
def liste_aleatoire(n):
    liste=[]
    for i in range (n):
        liste.append(random.randint(0,100000))
    return liste

def tri_insertion(L):
    """Tri par insertion (in-place).

    Principe : on parcourt la liste à partir du deuxième élément,
    et on insère chaque élément (= clé) à sa position correcte
    dans la partie gauche déjà triée en le décalant vers la gauche.

    Complexité : O(n^2) en pire cas, O(n) dans le meilleur cas (déjà triée).
    """
    N = len(L)
    for n in range(1, N):
        cle = L[n]
        j = n - 1
        while j >= 0 and L[j] > cle:
            L[j + 1] = L[j]  # décalage
            j = j - 1
        L[j + 1] = cle

def partition(L,debut,fin):
    """Partition pour le tri rapide (Quicksort) in-place.

    Principe : on choisit un pivot (ici L[fin]) et on réordonne
    les éléments de sorte que ceux <= pivot se trouvent à gauche
    et les > pivot à droite. Retourne l'indice final du pivot.

    Complexité partition : O(n) en temps.
    """
    pivot = L[fin]
    i = debut
    j = debut
    while j < fin:
        if L[j] <= pivot:
            L[i], L[j] = L[j], L[i]
            i += 1
        j += 1
    L[fin], L[i] = L[i], L[fin]
    return i
def tri_partition_recursif(L,debut,fin):
    """Quicksort récursif in-place.

    Principe : on partitionne la liste autour d'un pivot puis on trie
    récursivement les sous-listes gauche et droite.

    Complexité moyenne : O(n log n). Pire cas : O(n^2) (pivot mal choisi).
    """
    if debut < fin:
        i = partition(L, debut, fin)
        tri_partition_recursif(L, debut, i - 1)
        tri_partition_recursif(L, i + 1, fin)
def tri_partition(liste):
    """Wrapper pour Quicksort qui retourne une nouvelle liste triée.

    Copie l'entrée pour ne pas la modifier puis appelle la version
    récursive in-place.
    """
    L = list(liste)
    tri_partition_recursif(L, 0, len(L) - 1)
    return L

def tri_minimum(tab):
    n = len(tab)
    for i in range(n - 1):
        # Trouver l’indice du minimum dans la partie non triée
        indice_min = i
        for j in range(i + 1, n):
            if tab[j] < tab[indice_min]:
                indice_min = j
        # Échanger l’élément courant avec le minimum trouvé
        tab[i], tab[indice_min] = tab[indice_min], tab[i]
    """Tri par sélection (alias tri par minimum) in-place.

    Principe : pour chaque position i, on cherche le minimum dans
    la portion non triée et on l'échange avec la position i.

    Complexité : O(n^2) en temps, O(1) en espace additionnel.
    """
    return tab

def tri_selection(sequence):
    """Tri par sélection.
    Renvoie une nouvelle liste triée sans modifier l'originale.
    Le tri par sélection (selection sort) consiste à :

Parcourir la liste élément par élément.
1- À chaque position, chercher le plus petit élément restant dans la partie non triée.
2- Échanger l’élément courant avec ce minimum.
3- Recommencer jusqu’à ce que tout soit trié.
En résumé :À chaque étape, on sélectionne le minimum et on le met à sa place.
    
    """
    L = list(sequence)
    n = len(L)
    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            if L[j] < L[min_idx]:
                min_idx = j
        if min_idx != i:
            L[i], L[min_idx] = L[min_idx], L[i]
    return L

def tri_bulles(tab):
    """Tri à bulles (Bubble Sort) in-place.

    Principe : on parcourt la liste en comparant des paires adjacentes
    et on échange si elles sont dans le mauvais ordre. À chaque passe
    le plus grand élément « remonte » en fin de liste.

    Complexité : O(n^2) en moyenne et pire cas. Stable et simple.
    """
    n = len(tab)
    for i in range(n):
        echange = False
        for j in range(0, n - i - 1):
            if tab[j] > tab[j + 1]:
                tab[j], tab[j + 1] = tab[j + 1], tab[j]
                echange = True
        if not echange:
            break
    return tab

def tri_fusion(tab):
    """Tri par fusion (Merge Sort) - version fonctionnelle.

    Principe : on divise récursivement la liste en deux moitiés,
    on trie chacune puis on fusionne les deux listes triées.

    Complexité : O(n log n) en temps, nécessite O(n) espace auxiliaire.
    """
    if len(tab) <= 1:
        return tab

    milieu = len(tab) // 2
    gauche = tri_fusion(tab[:milieu])
    droite = tri_fusion(tab[milieu:])

    return fusion(gauche, droite)


def fusion(g, d):
    """Fusionne deux listes triées `g` et `d` en une seule liste triée.

    Utilisée par le tri par fusion. Parcourt les deux listes simultanément
    et prend à chaque étape le plus petit élément disponible.
    """
    res = []
    i = j = 0

    while i < len(g) and j < len(d):
        if g[i] <= d[j]:
            res.append(g[i])
            i += 1
        else:
            res.append(d[j])
            j += 1

    res.extend(g[i:])
    res.extend(d[j:])
    return res

def tri_rapide(tab):
    """Quicksort (implémentation fonctionnelle simple).

    Principe : choisir un pivot, séparer en trois listes (inférieur, égal,
    supérieur) puis trier récursivement les parties < et > et concaténer.

    Complexité moyenne : O(n log n). Pire cas : O(n^2) si pivot mal choisi.
    """
    if len(tab) <= 1:
        return tab

    pivot = tab[len(tab) // 2]
    gauche = [x for x in tab if x < pivot]
    centre = [x for x in tab if x == pivot]
    droite = [x for x in tab if x > pivot]

    return tri_rapide(gauche) + centre + tri_rapide(droite)

def tri_tas(tab):
    """Tri par tas (heap sort via heapq pour commodité).

    Principe : on insère tous les éléments dans un tas (heap) puis on
    extrait les éléments dans l'ordre croissant. Ici on utilise le
    module `heapq` pour obtenir un tri en O(n log n).
    """
    import heapq
    h = []

    for elem in tab:
        heapq.heappush(h, elem)

    return [heapq.heappop(h) for _ in range(len(h))]

def tri_denombr(tab):
    """Tri par dénombrement (Counting Sort).

    Principe : compte le nombre d'occurrences de chaque valeur entière
    entre 0 et max(tab), puis reconstruit la liste triée. Très efficace
    lorsque l'univers des valeurs (max-min) est raisonnable.

    Complexité : O(n + k) où k = max(tab).
    """
    if not tab:
        return tab

    maxi = max(tab)
    compte = [0] * (maxi + 1)

    for x in tab:
        compte[x] += 1

    res = []
    for valeur, occur in enumerate(compte):
        res.extend([valeur] * occur)

    return res

def tri_base(tab):
    """Tri radix (par base décimale) utilisant le comptage par chiffre.

    Principe : pour chaque position de chiffre (unités, dizaines, ...)
    on effectue un tri stable par comptage sur le chiffre courant.

    Complexité : O(d*(n + b)) où d = nombre de chiffres, b = base (ici 10).
    """
    if not tab:
        return tab

    exp = 1
    maxi = max(tab)

    while maxi // exp > 0:
        tab = comptage_digit(tab, exp)
        exp *= 10

    return tab


def comptage_digit(tab, exp):
    """Étape de comptage stable pour un chiffre donné (utilisé par radix).

    `exp` est 1 pour unités, 10 pour dizaines, etc. Produit une nouvelle
    liste triée par le chiffre courant tout en préservant la stabilité.
    """
    n = len(tab)
    sortie = [0] * n
    compte = [0] * 10

    for num in tab:
        digit = (num // exp) % 10
        compte[digit] += 1

    for i in range(1, 10):
        compte[i] += compte[i - 1]

    for i in range(n - 1, -1, -1):
        digit = (tab[i] // exp) % 10
        sortie[compte[digit] - 1] = tab[i]
        compte[digit] -= 1

    return sortie

##Ex2
if __name__ == '__main__':
    start_time = time.time()
    l = liste_aleatoire(10000)
    result = tri_tas(l)

    # Démonstration rapide de tri_selection
    sample = [64, 25, 12, 22, 11]
    print('Avant :', sample)
    print('tri_selection :', tri_selection(sample))

    end_time = time.time()
    print(f"Complexite en temps d'exécution: {end_time - start_time} seconds")

""" Tableau comparatif des tris :
Taille  | Insertions | Minimum | Bulles | Fusion  | Rapide | Tas   | Dénombrement | Base
10          0.00002    0.00004   0.00002   0.00003  0.00003  0.0015     0.012        0.00006
100         0.00027    0.0003    0.0004    0.00018  0.0002   0.0017     0.014        0.00022
1000        0.02761    0.0203    0.0445    0.0024   0.0018   0.0016     0.014        0.00144
10000       2.63628    1.9097    4.8372    0.0336   0.0246   0.0095     0.021        0.01618

##Ex10 --> pas tant de diffrence entre nlogn et n, n**2 bien plus long pour 10000
"""