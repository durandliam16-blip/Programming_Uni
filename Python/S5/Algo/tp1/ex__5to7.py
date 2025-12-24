##Ex5
def agregation():
    new,total=0,0
    min=10000000
    max=0
    i=0
    while new != None:
        new=int(input("Donne un chiffre: "))
        i+=1
        total=new+total
        moy=(total)/i
        if new>max:
            max=new
        if new<min:
            min=new
        print(f"Le minimum est {min}, le maximum est {max} et enfin on a la moyenne {moy}")

##Ex6
"""
Si n pair (ex 8) on represente equipe sous forme polygone avec l'equipe
    pivot au centre de la figure puis les autres aux noeuds.
    Step1: On tire trait horizontaux entre sommets (ex (1,7), (2,7) etc)
    Step2: Puis tourne dans sens horaire tout les noeuds (ex 1 passe de en haut à en haut à droite)
    Step3 On recommence
Si n impair (ex 7) on fait pareil en tournant autour pivot fictif (donc (2,7) et 1 joue pas premier mais joue contre equipe 2 ensuite)
Puis ajouter que equipe chez elles ou en déplacement"""

def generer_calendrier(nb_equipes):
    # Si le nombre d’équipes est impair, on ajoute une équipe fictive
    fictive = False
    if nb_equipes % 2 != 0:
        nb_equipes += 1
        fictive = True
    equipes = list(range(1, nb_equipes + 1)) #créer liste des équipes
    pivot = equipes[-1]  # dernière équipe = pivot
    nb_journees = nb_equipes - 1 

    for journee in range(1,nb_journees+1):
        print(f"\nJournée n'{journee}:")
        for i in range(nb_equipes // 2):
            e1 = equipes[i]
            e2 = equipes[-i - 1]
            if fictive and (e1 == nb_equipes or e2 == nb_equipes): # Si une équipe est fictive → repos
                if e1 == nb_equipes:
                    print(f"  équipe {e2} au repos")
                else:
                    print(f"  équipe {e1} au repos")
            else:
                #Inverse pour alterner domicile/extérieur
                if journee % 2 == 0:
                    print(f"  équipe {e1} reçoit équipe {e2}")
                else:
                    print(f"  équipe {e2} reçoit équipe {e1}")
        equipes = [equipes[0]] + [equipes[-1]] + equipes[1:-1]
        #le pivot reste en place, la dernière passe en 2 et remet autres
generer_calendrier(6)

def generer_calendrier2(n):
    # --- Étape 1 : ajouter équipe fictive si besoin ---
    if n % 2 != 0:
        n_prime = n + 1
        fictive = True
    else:
        n_prime = n
        fictive = False
    nb_journees = n_prime - 1
    nb_matchs_par_journee = n_prime // 2
    # --- Étape 2 : génération du calendrier selon les formules ---
    for j in range(1, nb_journees + 1):
        print(f"\nJournée n°{j}:")
        for i in range(1, nb_matchs_par_journee + 1):
            # Calcul des équipes locales et visiteuses selon la formule
            if i == 1:
                # --- FORMULE SPÉCIALE POUR LE PREMIER MATCH ---
                equipe_locale = n_prime if n_prime % 2 == 0 else 0
            else:
                equipe_locale = ((j + i - 2) % (n_prime - 1)) + 1
            equipe_visiteuse = ((j - i + n_prime - 1) % (n_prime - 1)) + 1
            # --- Étape 3 : afficher le résultat ---
            if fictive and (equipe_locale == n_prime or equipe_visiteuse == n_prime):
                # L'une est fictive → repos
                if equipe_locale == n_prime:
                    print(f"  équipe {equipe_visiteuse} au repos")
                else:
                    print(f"  équipe {equipe_locale} au repos")
            else:
                print(f"  équipe {equipe_locale} reçoit équipe {equipe_visiteuse}")

##Ex7
def transcriprion_calcul():
    formule = str(input("Donne ton calcul (format: ValOpéVal=): "))
    liste_ope=["+","*","%","/"]
    liste_nb,liste_val=[],[]
    ope,val="",""
    for j in range(0,10):
        liste_nb.append(str(j))
    if formule[-1]!="=":
        print("réessaye")
        formule=str(input("Donne ton calcul (format: ValOpéVal=): "))
    for i in range(0, len(formule)-1):
        lettre = formule[i]
        if lettre in liste_nb:
            val+=lettre
        elif lettre in liste_ope:
            ope+=lettre
            if val != "":
                liste_val.append(int(val))
                val=""
        else:
            formule = str(input("Donne ton calcul (format: ValOpéVal=): "))
    liste_val.append(int(val))
    if ope==liste_ope[0]:
        result=liste_val[0]+liste_val[1]
    if ope==liste_ope[1]:
        result=liste_val[0]*liste_val[1]
    if ope==liste_ope[2]:
        result=liste_val[0]%liste_val[1]
    if ope==liste_ope[3]+liste_ope[3]:
        result=liste_val[0]//liste_val[1]
    print(result)
