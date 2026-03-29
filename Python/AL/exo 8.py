import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad


# Question 3 et 4

# Affichage
x = np.linspace(-np.pi, np.pi, 500)
n1, n2 = 1, 1
plt.plot(x, np.cos(n1*x), label=f'cos({n1}x)')
plt.plot(x, np.sin(n2*x), label=f'sin({n2}x)')
plt.legend()
plt.title("Tracé de cos(x) et sin(x)")
plt.show()

# Produit scalaire
def produit_scalaire(n1, n2):
    integrand = lambda x: np.cos(n1*x) * np.sin(n2*x)
    valeur, erreur = quad(integrand, -np.pi, np.pi) 
    return valeur

print(f"<cos(x), sin(x)> = {produit_scalaire(1, 1):.5f}")
print(f"<cos(2x), sin(3x)> = {produit_scalaire(2, 3):.5f}")


# Question 6

def f_n(x, n):
    somme = np.zeros_like(x)
    for k in range(1, n + 1):
        harmonique = 2 * k - 1 
        somme += (1 / harmonique) * np.sin(harmonique * x)
    return (4 / np.pi) * somme

# Calcul des différentes fonctions
f1 = f_n(x, 1)
f2 = f_n(x, 2)
f3 = f_n(x, 3)
f15 = f_n(x, 15)


plt.subplot(1, 2, 2)
plt.plot(x, f1, label='f1(x)', linestyle=':', alpha=0.8)
plt.plot(x, f2, label='f2(x)', linestyle='--', alpha=0.8)
plt.plot(x, f3, label='f3(x)', linestyle='-.', alpha=0.8)
plt.plot(x, f15, label='f15(x)', color='black', linewidth=2)

plt.legend()
plt.title("Question 6")
plt.grid(True, linestyle='--', alpha=0.6)

plt.tight_layout()
plt.show()