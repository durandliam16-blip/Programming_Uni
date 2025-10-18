#Ex1 Q1
import util
import math
def disque ():
    ray=util.saisir_entier()
    surf=math.pi*ray*ray
    peri=math.pi*2*ray
    return peri,surf

#Ew1 Q2
def cylindre():
    peri,surf=disque()
    h=int(input("Donne la hauteur "))
    vol=surf*h
    return peri,surf,vol

#Ex2
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





