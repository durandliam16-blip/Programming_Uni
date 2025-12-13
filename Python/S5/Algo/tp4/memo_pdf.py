from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Fiche de Revision : Algorithmique & Structures', 0, 1, 'C')
        self.ln(10)

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.set_fill_color(200, 220, 255) # Bleu clair
        self.cell(0, 10, f'  {title}', 0, 1, 'L', 1)
        self.ln(4)

    def chapter_body(self, body):
        self.set_font('Arial', '', 11)
        self.multi_cell(0, 6, body)
        self.ln()

    def chapter_code(self, code):
        self.set_font('Courier', '', 9) # Police type code
        self.set_fill_color(240, 240, 240) # Gris clair
        self.multi_cell(0, 5, code, 1, 'L', 1)
        self.ln()

pdf = PDF()
pdf.add_page()

# --- CHAPITRE 1 : LES CLASSES ---
pdf.chapter_title('1. Les Classes en Python (Les Bases)')
pdf.chapter_body(
    "Une classe est un plan de construction (moule). L'objet est la maison construite.\n"
    "- __init__(self) : Le constructeur, appelé automatiquement à la création.\n"
    "- self : Référence à l'objet actuel (l'instance)."
)
pdf.chapter_code(
"""class Maillon:
    def __init__(self, valeur):
        self.valeur = valeur
        self.suivant = None

# Utilisation
m1 = Maillon(10)      # Instanciation
m1.suivant = Maillon(20) # Liaison"""
)

# --- CHAPITRE 2 : LISTES CHAINÉES ---
pdf.chapter_title('2. Listes Chainees vs Tableaux')
pdf.chapter_body(
    "TABLEAU PYTHON ([]):\n"
    "- Mémoire : Cases contiguës.\n"
    "- Ajout fin : Rapide O(1).\n"
    "- Retrait début (pop(0)) : LENT O(N) (nécessite de décaler tout le tableau).\n\n"
    "LISTE CHAINÉE (LinkedList):\n"
    "- Mémoire : Éléments dispersés reliés par des flèches (pointeurs).\n"
    "- Retrait début/fin : RAPIDE O(1) (on change juste une flèche)."
)

# --- CHAPITRE 3 : STRUCTURES LINEAIRES ---
pdf.chapter_title('3. Definitions : Pile, File, Deque')
pdf.chapter_body(
    "PILE (Stack) - LIFO (Last In, First Out) :\n"
    "- Comme une pile d'assiettes.\n"
    "- Opérations : push (empiler), pop (dépiler).\n\n"
    "FILE (Queue) - FIFO (First In, First Out) :\n"
    "- Comme une queue au supermarché.\n"
    "- Opérations : enqueue (enfiler), dequeue (défiler).\n\n"
    "DEQUE (Double Ended Queue) :\n"
    "- Structure universelle (File à deux bouts).\n"
    "- Performant pour ajouter/retirer des DEUX côtés (O(1))."
)

# --- CHAPITRE 4 : CODE REUTILISABLE ---
pdf.add_page()
pdf.chapter_title('4. CODE "BOOTSTRAP" (A COPIER/COLLER)')
pdf.chapter_body(
    "Voici l'implémentation professionnelle par COMPOSITION.\n"
    "Ce code utilise 'deque' de Python (optimisé C) pour créer des Piles et Files O(1).\n"
    "C'est la réponse attendue pour des implémentations robustes (Ex 6 du TP)."
)
pdf.chapter_code(
"""from typing import Any, Optional
from collections import deque

# --- LE MOTEUR (Wrapper universel) ---
class DequeWrapper:
    def __init__(self): self.items = deque()
    def add_tail(self, item): self.items.append(item)
    def add_head(self, item): self.items.appendleft(item)
    def remove_tail(self): 
        return self.items.pop() if self.items else None
    def remove_head(self): 
        return self.items.popleft() if self.items else None
    def is_empty(self): return len(self.items) == 0

# --- 1. LA PILE (STACK) - LIFO ---
class Stack:
    def __init__(self): 
        self.container = DequeWrapper() # Composition

    def push(self, item: Any): 
        self.container.add_tail(item)

    def pop(self) -> Optional[Any]: 
        return self.container.remove_tail() # Sortie même côté

    def is_empty(self) -> bool: 
        return self.container.is_empty()

# --- 2. LA FILE (QUEUE) - FIFO ---
class Queue:
    def __init__(self): 
        self.container = DequeWrapper()

    def enqueue(self, item: Any): 
        self.container.add_tail(item)

    def dequeue(self) -> Optional[Any]: 
        return self.container.remove_head() # Sortie côté opposé

    def is_empty(self) -> bool: 
        return self.container.is_empty()"""
)

pdf.output('Fiche_Revision_Algo.pdf')
print("✅ Fichier PDF généré : 'Fiche_Revision_Algo.pdf'")