from fractions import Fraction
# -----------------------------------------------------------------
# join lines d'une liste
# -----------------------------------------------------------------
def concatenate(lines): return "".join(lines)
# -----------------------------------------------------------------
# applique \n à un ensemble de chaines dans une liste
# -----------------------------------------------------------------
def newlines(lines): return "\n".join(lines)
# -----------------------------------------------------------------
# retourne le signe d'un nombre +,- 
# -----------------------------------------------------------------
def signstr(number):
    if abs(number) > 0 :
        return "+" if number.real>0 else "-"
    else:
        return ""
# -----------------------------------------------------------------
def absnum(number):
    if isinstance(number,int):
        return f"{abs(number)}"
    elif isinstance(number,float) :
        return f"{abs(number):.1e}"
# -----------------------------------------------------------------
def absfrac(number,imaginary=False):
    n=abs(number)
    num,den=Fraction(n).limit_denominator().as_integer_ratio()
    j=f"{'j' if imaginary else ''}"
    if num == 0 and imaginary :   return ""
    if den > 1 :
        if num == 1 and imaginary :   num,j="j",""
        return f"({num}/{den}){j}"
    else:
        if num == 1 and imaginary :   num,j="j",""
        return f"{num}{j}"
# -----------------------------------------------------------------
# retourne la chaine de la fraction de la valeur absolue des parties réelles et imaginaires
# si la partie imaginaire est égale à 1 on retourne simplement j
# -----------------------------------------------------------------
def strc(root):
    if abs(root.imag) > 0 :
        return (absfrac(root.real),absfrac(root.imag,imaginary=True))
    else:
        return (absfrac(root.real),'') 
# -----------------------------------------------------------------
# retourne la chaine de caractères du produit 
# de toute les racines (poles ou zeros)
# (p-racine_1)(p-racine_2)...(p-racine_n)
# -----------------------------------------------------------------
def strroot(roots):
    out=''
    for root in roots:
        r,i=strc(root)
        out+="(" 
        out+=f"p{signstr(-root.real) if root.real !=0 else '+'}{r}"
        out+=f"{signstr(-root.imag)}{i}"
        out+=")"
    return out
# -----------------------------------------------------------------
# retourne la chaine de caractères du polynome 
# coeff_k p^k + -racine_1)(p-racine_2)...(p-racine_n)
# -----------------------------------------------------------------
def strpoly(poly):
    out=[]
    for k,coeff in enumerate(poly):
        expo=len(poly)-k-1
        if coeff==0.0 :continue
        if k > 0 or coeff < 0:
            signcoeff=f"{signstr(coeff)}{absnum(coeff)}"
        else:
            signcoeff=f"{absnum(coeff)}"
        match expo:
            case 0:
                strexpo=""
                strcoeff=f"{signcoeff}"
            case 1 :
                strexpo=f"p"
                strcoeff=f"{signcoeff if coeff != 1 else signstr(coeff) if k!=0 else ''}"
            case _ :
                strexpo=f"p^{expo}"
                strcoeff=f"{signcoeff if coeff!=1 else ''}"
        out+=[f"{strcoeff}{strexpo}"]
    return concatenate(out)
