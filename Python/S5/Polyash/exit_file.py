#Liste à remplir au fur à mesure de l'algo :

#schedule = [ [ id_intersection, {rue,durée}, ... ], [2, {ruedenantes,2}, {ruedeangers,5}] ]
schedule=[[1, {"rue1":2}, {"rue2":3}], [2, {"rue3":4}], [3, {"rue4":1}, {"rue5":2}, {"rue6":3}]]


#Ecriture du fichier, après algo avec : 

with open("sortie.txt", "w") as rendu:
    nb_intersection=len(schedule)
    rendu.write(str(nb_intersection))
    rendu.write("\n")

    for i in range (nb_intersection):
        #note l'id de l'intersection
        intersection_id = schedule[i][0]  
        rendu.write(f"{intersection_id}\n")

        #note le nb de rues entrantes à cet intersection
        nb_rues = len(schedule[i]) - 1
        rendu.write(f"{nb_rues}\n")

        #note les rues entrantes et leur durée
        for j in range (1, len(schedule[i])):
            for key, value in schedule[i][j].items():
                rendu.write(f"{key}\t{value}\n")