##Ex1
from typing import ClassVar
#Q1
class Noeud:
    def __init__(self, valeur, g, d):
        self.val = valeur 
        self.g = g 
        self.d = d 

class Arbre:
    terminal : ClassVar[Noeud]= Noeud(None) 
    terminal.g=terminal
    terminal.d=terminal

    #Q3
    def __init__(rac, self, nodes: list[int | None] | None = None) -> 'BinaryTree':
        self.root=rac
        if not nodes:
            return Arbre()

        node_list = []
        for val in nodes:
            if val is None:
                node_list.append(self.terminal)
            else:
                node_list.append(Noeud(val))

        for i in range(len(nodes)):
            if node_list[i] is not None:
                left_index = 2 * i + 1
                right_index = 2 * i + 2
                if left_index < len(nodes):
                    node_list[i].left = node_list[left_index]
                if right_index < len(nodes):
                    node_list[i].right = node_list[right_index]

        return Arbre(node_list[0])
    
    #parcours en profondeur préfixe 
    def affpre(self): 
        if self.racine:
            print(self.racine.val)
            if self.racine.g:
                self.racine.g.affpre()
            if self.racine.d:
                self.racine.d.affpre()

    #Q2
    def isEmpty(self) -> bool:
        return self.racine is self.terminal
    def root(self) -> Noeud:
        return self.racine.val
    def terminal2(self) -> Noeud:
        return self.terminal

    #Q4
    def height(self) -> int:
        def height_tree(node): #car height na pas de para node
            if node is None:
                return 0
            else:
                return 1 + max(height_tree(node.left), height_tree(node.right))
        return height_tree(self.racine)
    def size(self) -> int:
        def size_tree(node): #car size na pas de para node
            if node is None:
                return 0
            else:
                return 1 + size_tree(node.left) + size_tree(node.right)
        return size_tree(self.racine)

a = Arbre(Noeud("x", 
        Arbre(Noeud("/",Arbre(Noeud("x")),Arbre(Noeud("-", Arbre(Noeud("x")) ,Arbre(Noeud(1,Arbre.terminal,Arbre.terminal)))))),
        Arbre(Noeud("+", Arbre(Noeud(78)),Arbre(Noeud("y",Arbre.terminal,Arbre.terminal))))))
arb = Arbre()
a.affpre()
print(a.root())











t = [2, 1, 4, 0, None, 3, 5]
bt = BinaryTree.make_tree(t)

print(bt.height())
print(bt.size())