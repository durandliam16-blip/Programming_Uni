#Extract document
data: str
with open('data_inventaire_prevert.txt ', "r") as infile: # ouverture du fichier (mode r: read)
    data = infile.read().upper()

#Aurait pu construire la liste en recupérant ceux diff de ; ou espace
liste_lettre=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","0","P","Q","R","S","T","U","V","W","X","Y","Z"]
liste_compt=[0]*len(liste_lettre)
#Faire le compte
for i in range (len(data)-1):
    if data[i] in liste_lettre:
        place = liste_lettre.index(data[i])
        liste_compt[place]+=1

#Afficher
import numpy as np
import matplotlib.pyplot as plt
plt.figure(figsize=(12,6))
plt.bar(liste_lettre, liste_compt)
plt.xlabel("Lettres")
plt.ylabel("Nombre d'apparitions")
plt.title("Fréquence des lettres")
plt.show()
