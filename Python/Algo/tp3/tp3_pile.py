##Ex1
pile=[1,2,3,4,5]
print(pile.append(10)) #push at end
print(pile.pop(0)) #pop 1st
print(pile)
print(pile[-1]) #see last
print(len(pile)) #see size
if pile:
    print("not empty") #check if empty
print(pile)

##Ex2
class Pile: 
    def __init__(self):
    #nécessaire pour les classes
        self.items = [] #pour l'objet actuel items = liste vide
    def push(self, val):
        self.items.append(val)
    def pop(self):
        if not self.isEmpty():
            return self.items.pop(-1) #haut pile
        raise IndexError("La pile est vide")
    def top(self):
        if not self.isEmpty():
            return self.items[-1]
        raise IndexError("La pile est vide") 
    def isEmpty(self):
        return len(self.items) == 0
    def size(self):
        return len(self.items)
p = Pile() #recup classe
p.push(1) #appel fonction
p.push(2)
p.push(3)
print(p.pop())
print(p.top())
print(p.size())
print(p.items)
print(p.isEmpty())     

##Ex3
#Q1 "( ( 4 - 3 ) * 2 ) + ( 5 / 2 )" est la forme infixe 
#Q2 "3 4 - 6 12 - / 7 2 + 6 / *" est la forme postfixe
#Q4
def post_to_infix(formule):
    result=Pile()
    l_ope=["+","-","*","/"]
    for elem in formule.split():
        if elem not in l_ope:
            result.push(elem)
        else:
            a,b=float(result.pop()),float(result.pop()) #pop prend le dernier item ad qui est le 2ème nb 
            if elem==l_ope[0]:
                result.push(a+b)
            elif elem==l_ope[1]:
                result.push(a-b)
            elif elem==l_ope[2]:
                result.push(a*b)
            elif elem==l_ope[3]:
                result.push(a/b)
    return result.top()
print(post_to_infix("3 4 - 6 12 - / 7 2 + 6 / *"))
