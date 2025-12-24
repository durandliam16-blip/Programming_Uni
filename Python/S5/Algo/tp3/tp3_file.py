##Ex6
file=[1,2,3,4,5]
print(file.append(10))
print(file.pop()) 
print(file)
print(file[0]) 
print(len(file)) 
if file:
    print("not empty")
print(file)

##Ex7
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

##Ex8
def inverse_file(file):
    prems=file.dequeue()
    if not file.isEmpty():
        inverse_file(file)
    file.enqueue(prems)
    return file

##Ex9
#probleme speciale
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
