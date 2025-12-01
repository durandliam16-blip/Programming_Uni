#Méthode TDD = Test faux > Simple solu pour simple > Refactoring
import unittest
from TDD_main import *

class TestTDD(unittest.TestCase):

    def test_q1_vide(self):
        self.assertEqual(q1(""), 0)
    def test_q1_solo(self):
        self.assertEqual(q1("5"), 5)
    def test_q1_double(self):
        self.assertEqual(q1("1,2"), 3)
    def test_many_q1(self):
        mes_tests = []
        for i in range (0,100):
            for j in range (0,100):
                mes_tests.append((f"{i},{j}", i+j))
        for value_in, value_out in mes_tests:
            with self.subTest(value_in=value_in, value_out=value_out):
                self.assertEqual(q1(value_in), value_out)
    
    def test_q2(self):
        self.assertEqual(q2("1,2,6"), 9)

    def test_q3_ok(self):
        self.assertEqual(q3("1\n2,3"), 6)
    def test_q3_erreur(self):
        self.assertEqual(q3("1,\n2"),None)

    def test_q4_ok(self):
        self.assertEqual(q4("//;\n1;2"),3)
    def test_q4_erreur(self):
        self.assertEqual(q4("/;\n1;2"),3)

    def test_q5(self):
        self.assertEqual(q5("2,1001"),2)