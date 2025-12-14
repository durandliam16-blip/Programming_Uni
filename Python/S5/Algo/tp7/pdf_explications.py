from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Explications du Code : TP7 Graphes', 0, 1, 'C')
        self.ln(10)

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.set_fill_color(200, 220, 255)
        self.cell(0, 6, title.encode('latin-1', 'replace').decode('latin-1'), 0, 1, 'L', 1)
        self.ln(4)

    def chapter_body(self, body):
        self.set_font('Arial', '', 11)
        self.multi_cell(0, 5, body.encode('latin-1', 'replace').decode('latin-1'))
        self.ln()

    def code_block(self, code):
        self.set_font('Courier', '', 9)
        self.set_fill_color(240, 240, 240)
        # Nettoyage basique pour l'affichage
        code = code.replace("    ", "  ") 
        self.multi_cell(0, 5, code.encode('latin-1', 'replace').decode('latin-1'), 1, 'L', 1)
        self.ln()

pdf = PDF()
pdf.add_page()

# --- PARTIE 1 : @PROPERTY ---
pdf.chapter_title('1. Le décorateur @property')
pdf.chapter_body(
    "Le décorateur @property en Python permet de transformer une méthode de classe en un "
    "attribut (variable) accessible sans utiliser de parenthèses ().\n\n"
    "Il sert principalement à trois choses dans ce TP :"
)

pdf.set_font('Arial', 'B', 11)
pdf.cell(0, 6, "A. Lisibilité (Syntaxe)", 0, 1)
pdf.set_font('Arial', '', 11)
pdf.multi_cell(0, 5, 
    "Il permet d'utiliser la syntaxe 'g.order' au lieu de 'g.order()'. "
    "Cela donne l'impression qu'on accède à une variable stockée, alors qu'en réalité, on exécute une fonction."
)
pdf.ln(2)

pdf.code_block(
"""class Graph:
  @property
  def order(self) -> int:
    return len(self.adj)

# Utilisation :
print(g.order)  # Pas de parenthèses !"""
)

pdf.set_font('Arial', 'B', 11)
pdf.cell(0, 6, "B. Attributs calculés (Dynamisme)", 0, 1)
pdf.set_font('Arial', '', 11)
pdf.multi_cell(0, 5, 
    "C'est le point crucial. L'ordre du graphe change quand on ajoute un sommet. "
    "Au lieu de maintenir manuellement une variable 'self.nb_sommets' (risque d'erreur), "
    "@property calcule la valeur à la volée (len(self.adj)) au moment où vous la demandez. "
    "La donnée est toujours à jour."
)
pdf.ln(2)

pdf.set_font('Arial', 'B', 11)
pdf.cell(0, 6, "C. Protection (Lecture seule)", 0, 1)
pdf.set_font('Arial', '', 11)
pdf.multi_cell(0, 5, 
    "Par défaut, on ne peut pas modifier une property. "
    "Ecrire 'g.order = 10' provoquera une erreur. Cela protège l'intégrité de vos données."
)
pdf.ln(5)

# --- PARTIE 2 : STRUCTURE DU CODE ---
pdf.chapter_title('2. Principes clés du code fourni')
pdf.chapter_body(
    "Le code peut sembler long car il gère tous les cas (orienté/non-orienté, pondéré/non-pondéré). "
    "Voici les 3 blocs logiques pour comprendre l'essentiel."
)

pdf.set_font('Arial', 'B', 11)
pdf.cell(0, 6, "Bloc 1 : La structure de données (Dictionnaire de Dictionnaires)", 0, 1)
pdf.set_font('Arial', '', 11)
pdf.multi_cell(0, 5, 
    "Choix technique ligne 158 : self.adj: Dict[str, Dict[str, int]] = {}\n"
    "Au lieu d'une liste de listes, on utilise des dictionnaires imbriqués.\n"
    "- self.adj['A'] donne les voisins de A.\n"
    "- self.adj['A']['B'] donne directement le POIDS de l'arête A->B.\n"
    "Avantage : Accès instantané en O(1) pour vérifier une connexion."
)
pdf.ln(2)

pdf.set_font('Arial', 'B', 11)
pdf.cell(0, 6, "Bloc 2 : Gestion Automatique (Orienté vs Non-Orienté)", 0, 1)
pdf.set_font('Arial', '', 11)
pdf.multi_cell(0, 5, 
    "L'utilisateur n'a pas besoin de gérer le miroir des arêtes. "
    "La méthode add_edge vérifie si le graphe est non-orienté et crée le retour automatiquement."
)
pdf.code_block(
"""def add_edge(self, u, v, weight=1):
  self.add_vertex(u) # Sécurité
  self.add_vertex(v)
  self.adj[u][v] = weight # Ajout u->v
  
  if not self.is_directed:
    self.adj[v][u] = weight # Ajout automatique v->u"""
)
pdf.ln(2)

pdf.set_font('Arial', 'B', 11)
pdf.cell(0, 6, "Bloc 3 : La Contraction (Passage complexe)", 0, 1)
pdf.set_font('Arial', '', 11)
pdf.multi_cell(0, 5, 
    "La fonction contract_edge(x, y) fusionne Y dans X.\n"
    "1. Redirection des entrants : Tout ce qui pointait vers Y pointe vers X.\n"
    "2. Transfert des sortants : Tout ce que Y visait, X le vise aussi.\n"
    "3. Gestion des conflits (Min) : Si X et Y avaient tous les deux une route vers Z, "
    "on conserve la route la plus courte (min)."
)
pdf.code_block(
"""# Logique simplifiée de fusion des poids
if z in self.adj[x]:
  # On garde le meilleur poids entre celui de X et celui venant de Y
  self.adj[x][z] = min(self.adj[x][z], poids_venant_de_y)
else:
  self.adj[x][z] = poids_venant_de_y"""
)

# --- PARTIE 3 : OUTILS PYTHON ---
pdf.ln(5)
pdf.chapter_title('3. Outils Python utilisés')

pdf.chapter_body(
    "* Type Hinting (: List[str], -> bool) : Ce sont des indications visuelles pour aider à la lecture "
    "et au débogage. Elles n'affectent pas l'exécution.\n"
    "* @classmethod (from_edge_list) : Une 'usine' qui permet de créer un graphe directement "
    "depuis une liste brute, sans faire 50 appels à add_edge.\n"
    "* del : Commande pour supprimer proprement une entrée dans un dictionnaire."
)

# Génération du fichier
output_filename = "explications_tp7_graphe.pdf"
pdf.output(output_filename)
print(f"Le PDF '{output_filename}' a été généré avec succès.")