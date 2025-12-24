text : str= 'Bonjour' #declare le type
word :str = 'le monde'
if text == 'Bonjour':
    word = 0o7

#enumeration de str
print(f'Dissection de la chaine de caracteres {repr(text)} :')
for i, c in enumerate(text):
    print(i, c)
