# suite de Collatz
u: int = 27
while u != 1:
    if u%2 !=0: # si u est impair:
        u = 3 * u + 1 # alors u est multiplie par 3, + 1
    else: # si u est pair:
        u /= 2 # alors u est divise par 2
print('La conjecture de Syracuse est verifiee !')
