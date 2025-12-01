data: str
with open('data_inventaire_prevert.txt ', "r") as infile: # ouverture du fichier (mode r: read)
    data = infile.read()
    ligne_data = data.replace(";", "\n")
    ligne_data=ligne_data.split("\n")
    for i in range (len(ligne_data)-1):
        ligne_data[i]=str(i+1)+"."+ligne_data[i]
    print(ligne_data)
with open('inventaire_prevert.txt', "w") as outfile:# ouverture du fichier (w: write)
    for i in ligne_data:
        outfile.write(i) # ´ecriture des donn´ees dans le fichier

        outfile.write("\n")
