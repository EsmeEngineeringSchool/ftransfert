import numpy as np
from fractions import Fraction
# -----------------------------------------------------------------
# join lines d'une liste
# -----------------------------------------------------------------
def concatenate(lines):
    return "".join(lines)
# -----------------------------------------------------------------
# applique \n à un ensemble de chaines dans une liste
# -----------------------------------------------------------------
def newlines(lines): return "\n".join(lines)
# -----------------------------------------------------------------
# -----------------------------------------------------------------
def beginmathdisplay():
    return "\["
def endmathdisplay():
    return "\]"
# -----------------------------------------------------------------
# retourne \macro{value}
# -----------------------------------------------------------------
def macro(name,value="",options="",semicolon=False):
    out=['\\'f"{name}"]
    if len(options) :
        out+=["["f"{options}""]"]
    if len(value) :
        out+=["{"f"{value}""}"]
    if semicolon : out[-1]+=";"
    return concatenate(out)
# ------------------------------------------------------------------------------
def draw(options,pt1,pt2,ptsep=" -- "):
    out=['\\'"draw"]
    if len(options) :
        out+=["["f"{options}""]"]
    if len(pt1) :
        out+=["("f"{pt1}"")"]
    if len(pt2):
        out+=[f"{ptsep}"]
        out+=["("f"{pt2}"")"]
    out[-1]+=";"
    return concatenate(out)
# -----------------------------------------------------------------
# retourne \begin{env}[options]
# -----------------------------------------------------------------
def begin(env,options=""):
    out=["\\begin{"f"{env}""}"]
    if len(options):
        out+=["["f"{options}""]"]
    return concatenate(out)
# -----------------------------------------------------------------
# retourne \end{env}
# -----------------------------------------------------------------
def end(env):
    return "\\end{"f"{env}""}"
# -----------------------------------------------------------------
# retourne le signe d'un nombre +,- 
# -----------------------------------------------------------------
def signstr(number):
    if abs(number) > 0 :
        return "+" if number.real>0 else "-"
    else:
        return ""
# -----------------------------------------------------------------
# -----------------------------------------------------------------
def absnum(number):
    if isinstance(number,int):
        return f"{abs(number)}"
    elif isinstance(number,float) :
        return f"{sci_latex(number,digits=0)}"
# -----------------------------------------------------------------
# retourne la chaine de caractères du produit 
# de toute les racines (poles ou zeros)
# (p-racine_1)(p-racine_2)...(p-racine_n)
# -----------------------------------------------------------------
def strroot(roots):
    out=''
    for root in roots:
        r,i=strc(root)
        out+="\\left("
        if len(i) : out+="\\left("
        out+=f"p{signstr(-root.real) if root.real !=0 else '+'}{r}"
        if len(i) : out+="\\right)"
        out+=f"{signstr(-root.imag)}{i}"
        out+="\\right)"
    return out
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
def absfrac(number,imaginary=False):
    n=abs(number)
    num,den=Fraction(n).limit_denominator().as_integer_ratio()
    j=f"{'j' if imaginary else ''}"
    if num == 0 and imaginary :   return ""
    if den > 1 :
        if num == 1 and imaginary :   num,j="j",""
        return "\\dfrac{"f"{num}""}""{"f"{den}""}"f"{j}"
    else:
        if num == 1 and imaginary :   num,j="j",""
        return f"{num}{j}"
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
# -----------------------------------------------------------------
# notation scientifique en LaTeX
# -----------------------------------------------------------------
def sci_latex(x, digits=1):
    if x == 0:
        return r"0"
    mantissa, exp = f"{x:.{digits}e}".split("e")
    inte=int(exp)+1
    if inte == 0 :
        return rf"0.{mantissa}"
    elif inte > -2 and inte < 0:
        return "0."+abs(inte)*"0"rf"{mantissa}"
    elif inte < 0 : 
        return rf"0.{mantissa}\cdot10^{{{inte}}}"
    else:
        if inte-1 == 0 :
            return rf"{mantissa}"
        else:
            return rf"{mantissa}\cdot10^{{{inte-1}}}"
# -----------------------------------------------------------------
def sci_latex_e(x, digits=1):
    return f"{x:.{digits}e}".replace("e", r"\mathrm{e}")
# ------------------------------------------------------------------------------
# génère des séquences geometriques ou arithmétiques : 
# arithmetic : xmin, xmin+q, xmin+2*q, xmin+3*q,...,xmax
# geometric  : xmin, xmin*q, xmin*q**2,xmin*q**3,...,xmax
# ------------------------------------------------------------------------------
def tick(xmin,xmax,sequence="geometric",raison=10):
    out="{"
    outvar=[]
    match sequence :
        case "geometric" :
            n=int(np.log10(xmax/xmin)/np.log10(raison))
            for k in range(n+1): outvar+=[f"{xmin*raison**k}"]
        case "arithmetic" :
            n=(xmax-xmin)//raison
            for k in range(n+1): outvar+=[f"{xmin+k*raison}"]
    out+=",".join(outvar)
    out+="}"
    return concatenate(out)
# ------------------------------------------------------------------------------
# génère les ticklabels 
# ------------------------------------------------------------------------------
def ticklabels(xmin,xmax,sequence="geometric",raison=10):
    out="{"
    outvar=[]
    match sequence :
        case "geometric" :
            raison=10
            n=int(np.log10(xmax/xmin)/np.log10(raison))
            for k in range(n+1) :
                expo=int(np.log10(xmin)+k)
                outvar+=["$10^{"f"{expo}""}$"]
        case _:
            return tick(xmin,xmax,sequence="arithmetic",raison=raison)
    out+=",".join(outvar)
    out+="}"
    return concatenate(out)
# -----------------------------------------------------------------
# Display matrix
# -----------------------------------------------------------------
def pmatrix(matrix):
    out=[begin("pmatrix")]
    for r in range(matrix.rows):
        for c in range(matrix.cols):
            out+=[str(sp.simplify(matrix[r,c])).replace("**","^").replace("*","")]+["&"]
        out.pop()
        out+=["\\\\"]
    out+=[end("pmatrix")]
    return newlines(out)
# -----------------------------------------------------------------
# Display plusieurs Matrices A\cdot B\cdot C ...
# -----------------------------------------------------------------
def multi_dot(matrices):
    out=[]
    for matrix in matrices :
        out+=[display_matrix_latex(matrix)]
        out+=["\\cdot"]
    out.pop()
    return newlines(out)
