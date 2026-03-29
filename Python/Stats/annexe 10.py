import numpy as np
import matplotlib.pyplot as plt

# Exercice 31

def simulation_temps_attente(_lambda, n_evenements=10000):
    temps_entre_evenements = np.random.exponential(1/_lambda, n_evenements)
    # Affichage
    plt.hist(temps_entre_evenements, bins=50, density=True, alpha=0.6, color='lightgreen')
    # Courbe théorique
    t = np.linspace(0, max(temps_entre_evenements), 100)
    pdf_theorique = _lambda * np.exp(-_lambda * t)
    plt.plot(t, pdf_theorique, 'r-', label=f'Loi exponentielle (λ={_lambda})')
    plt.title("Distribution des temps entre deux événements")
    plt.xlabel("Temps (t)")
    plt.ylabel("Densité de probabilité")
    plt.legend()
    plt.show()
simulation_temps_attente(_lambda=0.1)