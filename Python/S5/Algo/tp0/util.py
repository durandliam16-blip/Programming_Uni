def saisir_entier(invite: str = 'Saisir un nombre entier : ',escape: str | None = None) -> int | None:
    x=input(invite)
    try:
        if x==escape or x=="":
          return None
        else :
            return int(x)
    except ValueError:
        print("il faut un entier")
        saisir_entier()

if __name__=='__main__':
    print(saisir_entier("Ecrivez un nombre entier : "),"")
    pass
