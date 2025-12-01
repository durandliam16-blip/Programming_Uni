import numpy as np 
import random as rd

def game_of_life(size):
    M=ConfigInit(size)
    nb = int(input("Combien d'étapes veux-tu ? "))
    for i in range(nb):
        M = ChangeEtat(M,size)
        Imprime(M)

def ConfigInit(size):
    M=[]
    for i in range (size+2):
        ligne = []
        for j in range (size+2):
            if (i==0) or (i==size+1) or (j==0) or (j==size+1): 
            #verif si bordure
                ligne.append(0)
            else:
                ligne.append(rd.randint(0,1))
        M.append(ligne)
    return M

def ChangeEtat(M,size):
    M2 = [ligne.copy() for ligne in M]
    for i in range (1,size+1):
        for j in range (1, size+1):
            nb = nbVoisins(M,i,j)
            if (nb == 0) or (nb==4):
                M2[i][j]=0
            elif (nb==3) or (nb==2):
                M2[i][j]=1
    return M2 

def Imprime(M):
    print("\n",np.array(M))

def ImprimeDifference(M,M2,size):
    diff = [ligne.copy() for ligne in M]
    for i in range (1,size+1):
        for j in range (1, size+1):
            if (M[i][j] == 0) and (M2[i][j] == 1):
                diff[i][j]= "+1"
            if (M[i][j] == 1) and (M2[i][j] == 0):
                diff[i][j]= "-1"
            else: 
                diff[i][j]=0
    print("Les differences : ")
    print(np.array(diff))

def nbVoisins(M,i,j):
    compt = M[i][j+1] + M[i][j-1] +  M[i+1][j] + M[i-1][j]
    return compt

if __name__ == "__main__":
    game_of_life(4)