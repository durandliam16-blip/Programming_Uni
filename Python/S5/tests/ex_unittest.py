import unittest
#permet en faire plusieurs d'un coup et savoir lequel fail
#see more : https://docs.python.org/3/library/unittest.html#module-unittest

def incremente(x):
    return x + 1

class TestIncremente(unittest.TestCase):

    #exemple de test basique
    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_incremente(self):
        self.assertEqual(incremente(3), 4)
        
    def test_many_increments(self):
        for value_in, value_out in [
            (1, 2),
            (-100, -99),
            (-1, 0),
            (-1, 0),
            (0, 1),
            (100, 101),
        ]:
            with self.subTest(value_in=value_in, value_out=value_out):
                self.assertEqual(incremente(value_in), value_out)

#le lancer avec "python -m unittest ex_unittest.py"