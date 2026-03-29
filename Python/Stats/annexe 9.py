import numpy as np

# Exercice 28

def simulate_poisson_process(_lambda, time_steps):
    # _lambda: nombre moyen d'événement par unité de temps
    # time_steps: nombre de micro-intervalles dans la simulation
    # Calculate the probability of an event occurring in each time step
    p = _lambda / time_steps
    # Simulate the Poisson process using Bernoulli trials
    bernoulli_trials = np.random.rand(time_steps) < p
    # Count the number of successes (events)
    poisson_process_count = np.sum(bernoulli_trials)
    return poisson_process_count

def moyenne_result(_lambda, time_steps, taille):
    resultats = []
    for i in range(taille):
        resultats.append(simulate_poisson_process(_lambda, time_steps))
    moyenne_observee = np.mean(resultats)
    print(f"Valeur cible (Lambda) : {_lambda}")
    print(f"Moyenne de mes {taille} simulations : {moyenne_observee}")

if __name__ == "__main__":
    mon_lambda = 2.5 # Adjust this value based on your specific scenario
    moyenne_result(mon_lambda, time_steps=10000, taille=100)
    moyenne_result(mon_lambda, time_steps=10000, taille=1000)
    moyenne_result(mon_lambda, time_steps=10000, taille=10000)

# Exercice 29

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import poisson

# Paramètres 
mon_lambda = 4       # On s'attend à voir 4 événements en moyenne
m_simulations = 1000 # On répète l'expérience 1000 fois
n_steps = 1000       # Finesse du découpage temporel

resultats = [simulate_poisson_process(mon_lambda, n_steps) for _ in range(m_simulations)]

# Histo des résults
plt.hist(resultats, bins=range(max(resultats)+2), density=True, alpha=0.5, color='skyblue', label='Simulation (Pratique)', align='left')

# Loi de Poisson théorique
k_values = np.arange(0, max(resultats) + 1)
loi_theorique = poisson.pmf(k_values, mon_lambda)

# Affichage 
plt.plot(k_values, loi_theorique, color='red', marker='o', linestyle='-', zorder=3, label=f'Loi de Poisson (λ={mon_lambda})')
plt.title(f"Conparaison avec loi théorique (m={m_simulations})")
plt.xlabel("Nombre d'occurations")
plt.ylabel("Probabilité")
plt.legend()
plt.show()

# Exercice 30

#Paramètres :
lambdas = [1, 3, 10]
fig, axes = plt.subplots(1, 3, figsize=(15, 5)) # Créer la figure avec 3 sous-graphs
fig.suptitle('Distributions de Poisson pour différentes valeurs de λ')
x_max = 20  # Ajuster selon les besoins
x = np.arange(0, x_max + 1)

# Affichage
for i, _lambda in enumerate(lambdas):
    poisson_pmf = poisson.pmf(x, _lambda)
    axes[i].bar(x, poisson_pmf, align='center', color='lightblue', alpha=0.7)
    axes[i].set_xlabel('Nombre d\'événements')
    axes[i].set_ylabel('Probabilité')
    axes[i].set_title(f'λ = {_lambda}')
    axes[i].grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
