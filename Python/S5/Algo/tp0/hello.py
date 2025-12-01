text = 'Bonjour'
word = 'le monde'
if text == 'Bonjour':
    word = 0o7
text += ' ' + word
print(text)

print(f'Dissection de la chaine de caracteres {repr(text)} :')
for i, c in enumerate(text):
    print(i, c)
