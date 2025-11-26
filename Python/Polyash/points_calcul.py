#Liste à remplir au moment ou les voitures arrivent à destination :

#finishers = [ {id_voiture : temps_avant_fin_simu}, {...}, ... ]
finishers = [{1:2}, {2:3}, {3:0}]
award_par_arrivee=1000 #depend classe infoChallenge


#Calcul pour toutes le voitures: 

def result(finishers, award_par_arrivee):
    total=0
    nb_finishers=len(finishers)
    if nb_finishers==0:
        return 0
    else:
        for i in range (nb_finishers):
            for key, value in finishers[i].items():
                #F + (D – T) points if T ≤ D
                total += award_par_arrivee + value
        return total