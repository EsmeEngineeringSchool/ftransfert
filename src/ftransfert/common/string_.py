# -----------------------------------------------------------------
# join lines d'une liste
# -----------------------------------------------------------------
def concatenate(lines):
    return "".join(line for line in lines)
# -----------------------------------------------------------------
# applique \n à un ensemble de chaines dans une liste
# -----------------------------------------------------------------
def newlines(lines):
    return "\n".join(line for line in lines)

# -----------------------------------------------------------------
# retourne le signe d'un nombre +,- 
# -----------------------------------------------------------------
def signstr(number):
    return "+" if number.real>0 else "-"
# -----------------------------------------------------------------
# retourne la chaine du int de la valeur absolue des parties réelles et imaginaires
# si la partie imaginaire est égale à 1 on retourne simplement j
# -----------------------------------------------------------------
def strc(root):
    return (str(int(abs(root.real))),'j') if abs(root.imag) == 1.0 else (str(int(abs(root.real))),str(int(abs(root.imag)))+'j')
# -----------------------------------------------------------------
# retourne la chaine de caractères du produit 
# de toute les racines (poles ou zeros)
# -----------------------------------------------------------------
def strroot(roots):
    out=''
    for root in roots:
        r,i=strc(root)
        out+=f"(p{signstr(-root.real)}{r}{signstr(-root.imag)}{i})"
    return out
