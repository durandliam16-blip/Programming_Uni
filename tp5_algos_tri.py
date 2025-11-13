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

def fusion(L1,L2):
    n1 = len(L1)
    n2 = len(L2)
    L12 = [0]*(n1+n2)
    i1 = 0
    i2 = 0
    i = 0
    while i1<n1 and i2<n2:
        if L1[i1] < L2[i2]:
            L12[i] = L1[i1]
            i1 += 1
        else:
            L12[i] = L2[i2]
            i2 += 1
        i += 1
    while i1<n1:
        L12[i] = L1[i1]
        i1 += 1
        i += 1
    while i2<n2:
        L12[i] = L2[i2]
        i2 += 1
        i += 1 
    return L12
def tri_fusion_recursif(L):
    n = len(L)
    if n > 1:
        p = int(n/2)
        L1 = L[0:p]
        L2 = L[p:n]
        tri_fusion_recursif(L1)
        tri_fusion_recursif(L2)
        L[:] = fusion(L1,L2)
def tri_fusion(L):
    M = list(L)
    tri_fusion_recursif(M)
    return M

def fusion(L):
    n = len(L)
    if n > 1:
        p = int(n/2)
        L1 = L[0:p]
        L2 = L[p:n]
        fusion(L1)
        fusion(L2)
        L[:] = fusion(L1,L2)

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



start_time = time.time()
l=liste_aleatoire(10)
result = tri_partition(l)
end_time = time.time()
print(f"Complexite en temps d'ex ́ecution: {end_time - start_time} seconds")

""" Tableau comparatif des tris :
Taille  | Insertions | Minimum | Bulles | Fusion  | Rapide | Tas   | Dénombrement | Base
10          0.00002
100         0.00027
1000        0.02761
10000       2.63628
"""