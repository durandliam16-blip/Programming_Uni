import random
import time

def liste_aleatoire(n):
    liste=[]
    for i in range (n):
        liste.append(random.randint(0,100000))
    return liste



def tri_insertion(L):
    N = len(L)
    for n in range(1,N):
        cle = L[n]
        j = n-1
        while j>=0 and L[j] > cle:
            L[j+1] = L[j] # decalage
            j = j-1

def partition(L,debut,fin):
    pivot = L[fin]
    i = debut
    j = debut
    while j < fin:
        if L[j] <= pivot:
            L[i],L[j] = L[j],L[i]
            i += 1
        j += 1
    L[fin],L[i] = L[i],L[fin]
    return i
def tri_partition_recursif(L,debut,fin):
    if debut < fin:
        i = partition(L,debut,fin)
        tri_partition_recursif(L,debut,i-1)
        tri_partition_recursif(L,i+1,fin)
def tri_partition(liste):
    L = list(liste)
    tri_partition_recursif(L,0,len(L)-1)
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
    return tab

def tri_bulles(tab):
    n = len(tab)
    for i in range(n):
        # On détecte si un échange a eu lieu
        echange = False
        for j in range(0, n - i - 1):
            if tab[j] > tab[j + 1]:
                tab[j], tab[j + 1] = tab[j + 1], tab[j]
                echange = True
        # Si aucun échange : la liste est déjà triée, on arrête
        if not echange:
            break
    return tab

def tri_fusion(tab):
    if len(tab) <= 1:
        return tab
    
    milieu = len(tab) // 2
    gauche = tri_fusion(tab[:milieu])
    droite = tri_fusion(tab[milieu:])
    
    return fusion(gauche, droite)


def fusion(g, d):
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
    if len(tab) <= 1:
        return tab
    
    pivot = tab[len(tab) // 2]
    gauche = [x for x in tab if x < pivot]
    centre = [x for x in tab if x == pivot]
    droite = [x for x in tab if x > pivot]
    
    return tri_rapide(gauche) + centre + tri_rapide(droite)

def tri_tas(tab):
    import heapq
    h = []
    
    for elem in tab:
        heapq.heappush(h, elem)
    
    return [heapq.heappop(h) for _ in range(len(h))]

def tri_denombr(tab):
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
    if not tab:
        return tab
    
    exp = 1
    maxi = max(tab)
    
    while maxi // exp > 0:
        tab = comptage_digit(tab, exp)
        exp *= 10
    
    return tab


def comptage_digit(tab, exp):
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


start_time = time.time()
l=liste_aleatoire(10000)
result = tri_tas(l)
end_time = time.time()
print(f"Complexite en temps d'ex ́ecution: {end_time - start_time} seconds")

""" Tableau comparatif des tris :
Taille  | Insertions | Minimum | Bulles | Fusion  | Rapide | Tas   | Dénombrement | Base
10          0.00002    0.00004   0.00002   0.00003  0.00003  0.0015     0.012        0.00006
100         0.00027    0.0003    0.0004    0.00018  0.0002   0.0017     0.014        0.00022
1000        0.02761    0.0203    0.0445    0.0024   0.0018   0.0016     0.014        0.00144
10000       2.63628    1.9097    4.8372    0.0336   0.0246   0.0095     0.021        0.01618

== pas tant de diffrence entre nlogn et n, n**2 bien plus long pour 10000
"""