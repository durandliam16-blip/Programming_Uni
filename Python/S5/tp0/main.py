import util
import arithmetique as art

n: int = util.saisir_entier()
if not art.est_pair(n):
    n +=1
print(f"Somme de 0 `a {n} = {art.somme(n)}")
