#Q1
def somme(n: int) -> int:
    return n*(n+1)/2
print(somme(3))

#Q3 bis
def moyenne(valeurs):
    if not valeurs:
        return None  # ou 0, selon ce que tu préfères
    return sum(valeurs) / len(valeurs)

#Q4
def est_div_par(n,k):
    if n%k==0:
        return True
    else:
        return False

#Q5
def est_pair(a):
    print(est_div_par(a,2))

#Q6
def compris_dans(a,b,c):
    if a<b and b<=c:
        return True
    else:
        return False
print(compris_dans(1,2,2))
#suite de la Q pas fait

# section ex´ecut´ee uniquement si le module *est* le programme principal
if __name__ == '__main__':
# placer les tests (programme) ici
# attention `a l'indentation
    pass
