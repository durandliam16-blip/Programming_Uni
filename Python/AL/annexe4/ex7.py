import numpy as np

# On suppose que les 2 vecteurs sont linéairements indépendants
u1 = (0,1)
u2 = (2,1)

# 1- On vérifie qu'ils sont orthogonales
# cad si le produit scalaire est nul
scal = np.dot(u1, u2)
if scal == 0:
    print("Les vecteurs sont orthogonaux")
else:
    print("Les vecteurs ne sont pas orthogonaux")

# 2- On vérifie qu'ils sont normés 

norme_u1 = np.sqrt(np.dot(u1, u1))
norme_u2 = np.sqrt(np.dot(u2, u2))

    # Si non, on les divise par leur norme
if norme_u1 == 1:
    print("u1 est normé")
else : 
    print("u1 n'est pas normé")
    u1 = u1/norme_u1
    print("u1 ok")
if norme_u2 == 1:
    print("u2 est normé")
else : 
    print("u2 n'est pas normé")
    u2 = u2/norme_u2
    print("u2 ok")

# 3- Vérifie engendre le meme espace que les vecteurs initiaux
# "Si dim(Vect(u,v))=2 et que e1​,e2 sont dans cet espace et sont orthogonaux, alors ils forment forcément une base du même espace."