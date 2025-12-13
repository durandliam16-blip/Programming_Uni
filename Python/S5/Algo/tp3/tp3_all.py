#Ex1
pile=[1,2,3,4,5]
print(pile.append(10)) #push at end
print(pile.pop(0)) #pop 1st
print(pile)
print(pile[-1]) #see last
print(len(pile)) #see size
if pile:
    print("not empty") #check if empty
print(pile)

#Ex2
class Pile: 
    def __init__(self):
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
p = Pile()
p.push(1)
p.push(2)
p.push(3)
print(p.pop())
print(p.top())
print(p.size())
print(p.items)
print(p.isEmpty())     

#Ex3
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

#Ex6
file=[1,2,3,4,5]
print(file.append(10))
print(file.pop()) 
print(file)
print(file[0]) 
print(len(file)) 
if file:
    print("not empty")
print(file)

#Ex7
class File:
    def __init__(self):
        self.items = [] 
    def enqueue(self, val):
        self.items.append(val) #ajoute à la fin
    def dequeue(self):
        if not self.isEmpty():
            return self.items.pop(0) #enlève au début
        raise IndexError("La file est vide")
    def front(self):
        if not self.isEmpty():
            return self.items[0] #voir le 1er
        raise IndexError("La file est vide") 
    def isEmpty(self):
        return len(self.items) == 0
    def size(self):
        return len(self.items)
f = File()
f.enqueue(1)
f.enqueue(2)     
f.enqueue(3)
print(f.dequeue())
print(f.front())
print(f.size())    
print(f.items)
print(f.isEmpty())

#Ex8
def inverse_file(file):
    prems=file.dequeue()
    if not file.isEmpty():
        inverse_file(file)
    file.enqueue(prems)
    return file

#Ex9
def josephus(n,k):
    f=File()
    for i in range(1,n+1): #met tous dans la file
        f.enqueue(i)
    while f.size()>1: #tant qu'on a pas le dernier survivant
        for j in range(k-1):
            f.enqueue(f.dequeue()) #les k-1 sont safe donc end
        f.dequeue() #mort
    return f.front()
print(josephus(7,3))
