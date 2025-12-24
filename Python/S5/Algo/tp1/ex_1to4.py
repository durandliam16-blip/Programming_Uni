##Ex1 
#Q1
import tp0.util
import math
def disque ():
    ray=tp0.util.saisir_entier()
    surf=math.pi*ray*ray
    peri=math.pi*2*ray
    return peri,surf

#Q2
def cylindre():
    peri,surf=disque()
    h=int(input("Donne la hauteur "))
    vol=surf*h
    return peri,surf,vol

##Ex2
def determinant(a,b,c):
    delta=b*b-4*a*c
    return delta
def eqn_second_degre(a, b, c):
    delta=determinant(a,b,c)
    if delta==0:
        result=-b/2*a
        return result
    elif delta>0:
        result1=(-b-math.sqrt(delta))/(2*a)
        result2 = (-b+math.sqrt(delta)) / (2 * a)
        return result1,result2
    else:
        print("pas de racine réel")
print(eqn_second_degre(-1,5,14))

##Ex3
import random
def devine_nb():
    nb=random.randint(1,100)
    guess=1000
    while guess!=nb:
        guess=int(input("Devine le nombre "))
        if guess==nb:
            print("bravo")
        elif guess>nb:
            print("nb est plus petit")
        else:
            print("nb est plus grand")

##Ex4
def choisit_nb():
    nb=int(input("choisit un nombre entre 1 et 100 "))
    guess=random.randint(1,100)
    min,max=1,100
    L=[]
    while guess!=nb:
        if guess in L:
            print("tricheur")
        L.append(guess)
        print("mon guess est ",guess)
        rep_user=int(input("0 si nb plus petit et 1 si nb plus grand: "))
        if rep_user==1:
            min=guess
            guess=int((min+max)/2)
        else:
            max = guess
            guess = int((max + min) / 2)
    print("bravo")