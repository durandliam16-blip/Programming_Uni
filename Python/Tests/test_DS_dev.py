import unittest
def soustraction(n):
    return n-1
class TestSoustraction(unittest.TestCase):
    def test_simple(self):
        self.assertEqual(soustraction(8),7)
    def test_boucle(self):
        l=[]
        for i in range (1,10):
            l.append((i,i-1))
        for key, value in l:
            with self.subTest (key=key,value=value):
                self.assertEqual(soustraction(key), value)
#lancer avec python -m unittest namefichier.py

#mesurer cout (dynamique) 
    #pip install cProfile
    #python -m cProfile .\namefichier.py 

#verif écriture (statique)
    #pip install pep8 
    #python -m pep8 .\namefichier.py 

#check partie utile (statique)
    #pip install coverage
    #python -m coverage run -m unittest namefichier.nameclass.namefonction
    #python -m coverage report -m