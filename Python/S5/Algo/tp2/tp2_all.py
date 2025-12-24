##Ex1
def facto(n):
    if n==1 or n==0:
        return 1
    else:
        return n*facto(n-1)

##Ex2
def pgcd(a,b):
    if b==0:
        return a
    else:
        return(pgcd(b,a%b))

##Ex3
#Q1
def fibo(n):
    if n==0:
        return 0
    elif n==1:
        return 1
    else:
        return (fibo(n-1)+fibo(n-2))

#Q2
liste=[]
for i in range(0,40):
    liste.append(fibo(i))

#Q3
"""
F6
├── F5
│   ├── F4
│   │   ├── F3
│   │   └── F2
│   └── F3
└── F4
    ├── F3
    └── F2
"""

#Q4
def fibo2(n):
    if n==0:
        return 0
    elif n==1:
        return 1
    else:
        a,b=0,1
        for i in range (2,n+1):
            a,b=b,a+b
        return b
#Q5
print([fibo2(i) for i in range(20)])

##Ex4
#Q1-2
"""quotient de div de n par 10 donne le nb de dizaines de n (5478 donne 547)"""
def nb_digits(n: int,base) -> int:
    if n ==0:
        return 1
    compt=0
    while n>0:
        n=n//base
        compt+=1
    return compt

#Q3
def convert(n: int, base: int) -> str:
    if n<base:
        print(n)
    else:
        convert(n//base,base)
        print(n%base)

#Q4
def convert_mirror(n,base):
    if n<base:
        print(n)
    else:
        print(n%base)
        convert(n//base,base)

#Ex5
#Q1
def binom(n:int,k:int)->int:
    if k==0 or n==k:
        return 1
    return binom(n-1,k-1)+binom(n-1,k)

#Q2
#print(binom(100,50)) trop long

#Q3
def binom_memo(n:int,k:int,dico)->int:
    if k==0 or n==k:
        return 1
    if (n,k) in dico:
        return dico[(n,k)]
    else:
        dico[(n,k)]= binom_memo(n-1,k-1,dico)+binom_memo(n-1,k,dico)
    return dico[(n,k)]

##Ex6
def robot_cupide(damier: list[list[int]],trajet ,x: int =0, y: int =0) -> int:
    trajet[(x, y)] = damier[x][y]
    if x==len(damier)-1 or y==len(damier[0])-1:
        if x==len(damier)-1 and y==len(damier[0])-1:
            return trajet
        elif y==len(damier[0])-1:
            return robot_cupide(damier, trajet, x + 1, y)
        else:
            return robot_cupide(damier, trajet, x, y + 1)
    else:
        if damier[x + 1][y] >= damier[x][y+1]:
            return robot_cupide(damier,trajet,x+1,y) #descend
        else:
            return robot_cupide(damier,trajet,x,y+1) #decale
#print(robot_cupide([[1,2,3],[4,5,6],[7,8,9]],{}))

##Ex7
def hanoi(n,source,target,aux):
    if n== 1:
        print(f"deplace le disque 1 de {source} vers {target}")
        return
    hanoi(n-1,source,aux,target)
    print(f"deplace le disque {n} de {source} vers {target}")
    hanoi(n-1,aux,target,source)
#hanoi(2,"Pique 1", "Pique 2", "Pique 3")

#Ex9
from math import *
import numpy as np
import matplotlib.pyplot as plt

def triangle(x,y,c):
   plt.fill([x,x+c,x+c/2],[y,y,y+c*np.sqrt(3)/2],"b")
def t2s(n,x,y,c):
   if n==0:
       return triangle(x, y, c)
   else:
       t2s(n-1,x, y, c/2)
       t2s(n-1,c/2+x,y,c/2)
       t2s(n-1,c/4+x,(c/2)*sqrt(3)/2+y,c/2)
t2s(3,0,0,1)
plt.plot()
plt.show()
triangle(0,0,1) #figure1
tds(2) #figure 2
t2s(0,0,1,2)
