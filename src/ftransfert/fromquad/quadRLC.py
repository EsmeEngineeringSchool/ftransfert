import sys
import random
import sympy as sp
from functools import reduce
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
# retourne \macro{value}
# -----------------------------------------------------------------
def ltx(macro,value="",options=""):
    out=['\\'f"{macro}"]
    if len(options) :
        out+=["["f"{options}""]"]
    if len(value) :
        out+=["{"f"{value}""}"]
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
# tikz Quadripole (tous les composants sont identiques)
#   * -- SERIE -- * -- * -- SERIE -- * ----- *
#                 |                    |     |
#               SHUNT                SHUNT  SHUNT 
#                 |                    |     |
#   * ----------- * ---- * ----------- * --- *
# si dernier quadripole SHUNT peut être doublé 
# -----------------------------------------------------------------
def quad(n,pos,serie="R",shunt="R",first=False,last=False,):
    e,s=1,2
    out=[begin("scope","shift={("f"{4*pos}"",0)}")]
    out+=[ltx("draw")]
    out+=["(0,0) to [short, *-] (4,0)"]
    out+=["(0,3) to ["f"{serie[0]}=${serie}$""] (4,3)"]
    out+=["(4,0) to ["f"{shunt[0]}=${shunt[0]}$"",*-*] (4,3)"]
    if last :
        if len(shunt)>1 :
            out+=["(4,0) to [short, *-] (5.5,0)"]
            out+=["(4,3) to [short, *-] (5.5,3)"]
            out+=["(5.5,0) to ["f"{shunt[1]}=${shunt[1]}$"",*-*] (5.5,3)"]
            out+=["(6.2,0) to [open,v_>=$V_{"f"{s}""}$] (6.2,3)"]
        else:
            out+=["(5,0) to [open,v_>=$V_{"f"{s}""}$] (5,3)"]
        out+=["(3,3) to [short, -* ,i=$I_{"f"{s}""}$] (4,3)"]
    if first :
        out+=["(0,3) to [short, *- ,i=$I_{"f"{e}""}$] (1,3)"]
        out+=["(0,0) to [open,v^>=$V_{"f"{e}""}$] (0,3)"]
    out+=[";"]
    out+=[end("scope")]
    return newlines(out)
# -----------------------------------------------------------------
# tikz Quadripole (tous les composants sont différents)
# 
#   * -- SERIE_1 -- * -- * -- SERIE_2 -- * ---- *
#                 |                    |        |
#               SHUNT_1              SHUNT_2  SHUNT_3 
#                 |                    |        |
#   * ----------- * ---- * ----------- * ------ *
# si dernier quadripole SHUNT peut être doublé 
# -----------------------------------------------------------------
def quad_diff(n,pos,cc,serie="R",shunt="R",first=False,last=False):
    #print("debug",cc,file=sys.stderr)
    e,s=1,2
    out=[begin("scope","shift={("f"{4*pos}"",0)}")]
    out+=[ltx("draw")]
    out+=["(0,0) to [short, *-] (4,0)"]
    if last : 
        if serie == shunt :
            out+=["(0,3) to ["f"{serie[0]}=${serie[0]}_{cc[serie]}$""] (4,3)"]
        else:
            out+=["(0,3) to ["f"{serie[0]}=${serie[0]}_{cc[serie]}$""] (4,3)"]
        out+=["(4,0) to ["f"{shunt[0]}=${shunt[0]}_{cc[shunt[0]]+1}$"",*-*] (4,3)"]
        if len(shunt)>1 :
            out+=["(4,0) to [short, *-] (5.5,0)"]
            out+=["(4,3) to [short, *-] (5.5,3)"]
            if shunt[0] == shunt[1] :
                out+=["(5.5,0) to ["f"{shunt[1]}=${shunt[1]}_{cc[shunt[1]]+2}$"",*-*] (5.5,3)"]
            else:
                out+=["(5.5,0) to ["f"{shunt[1]}=${shunt[1]}_{cc[shunt[1]]+1}$"",*-*] (5.5,3)"]
            out+=["(6.2,0) to [open,v_>=$V_{"f"{s}""}$] (6.2,3)"]
        else:
            out+=["(5,0) to [open,v_>=$V_{"f"{s}""}$] (5,3)"]
        out+=["(3,3) to [short, -* ,i=$I_{"f"{s}""}$] (4,3)"]
    else:
        if serie == shunt :
            out+=["(0,3) to ["f"{serie[0]}=${serie[0]}_{cc[serie]-1}$""] (4,3)"]
        else:
            out+=["(0,3) to ["f"{serie[0]}=${serie[0]}_{cc[serie]}$""] (4,3)"]
        out+=["(4,0) to ["f"{shunt[0]}=${shunt[0]}_{cc[shunt[0]]}$"",*-*] (4,3)"]
    if first :
        out+=["(0,3) to [short, *- ,i=$I_{"f"{e}""}$] (1,3)"]
        out+=["(0,0) to [open,v^>=$V_{"f"{e}""}$] (0,3)"]
    out+=[";"]
    out+=[end("scope")]
    return newlines(out)
# -----------------------------------------------------------------
# Create a tranfert matrix serie ou shunt  
# -----------------------------------------------------------------
def transfert_matrix(Z,qtype="serie"):
    match qtype :
        case "serie" :
            return sp.Matrix([[1,Z],[0,1]])
        case "shunt" :
            return sp.Matrix([[1,0],[1/Z,1]])
# -----------------------------------------------------------------
# Display matrix  
# -----------------------------------------------------------------
def display_matrix_latex(matrix):
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
def display_multi_dot_latex(matrices):
    out=[]
    for matrix in matrices :
        out+=[display_matrix_latex(matrix)]
        out+=["\\cdot"]
    out.pop()
    return newlines(out)
# -----------------------------------------------------------------
# Retourne la substitution d'égalité de composant 
#  ZRX -> R
#  ZCX -> 1/Cp
#  ZLX -> Lp
#  YRX -> 1/R
#  YCX -> Cp
#  YLX -> 1/Lp
#   RX -> R
#   CX -> C
#   LX -> L
# -----------------------------------------------------------------
def get_substitutions_equal(symbols):
    substitution={}
    p=symbols["p"]
    for symb in symbols.keys():
        if symb in "pRLC" : continue
        if len(symb) == 2 :
            ZY,index=symb
        elif len(symb) == 3 :
            ZY,composant,index=symb
        match ZY :
            case "Z" :
                match composant:
                    case "R" :
                        sub=symbols["R"]
                    case "C" :
                        sub=1/(symbols["C"]*p)
                    case "L" :
                        sub=symbols["L"]*p
            case "Y" :
                match composant :
                    case "R" :
                        sub=1/(symbols["R"])
                    case "C" :
                        sub=symbols["C"]*p
                    case "L" :
                        sub=1/(symbols["L"]*p)
            case _ :
                sub=symbols[symb[0]]
        substitution.update({symb : sub})
        #print(f"{symb} -> {sub}")
    return substitution
# -----------------------------------------------------------------
# Retourne la substitution de base:
#  ZRX -> RX
#  ZCX -> 1/CXp
#  ZLX -> LXp
#  YRX -> 1/RX
#  YCX -> CXp
#  YLX -> 1/LXp
#   RX -> RX
#   CX -> CX
#   LX -> LX
# -----------------------------------------------------------------
def get_substitutions(symbols):
    substitution={}
    p=symbols["p"]
    for symb in symbols.keys():
        if len(symb) < 2:  continue
        if len(symb) == 2 :
            ZY,index=symb
        elif len(symb) == 3 :
            ZY,composant,index=symb
        match ZY :
            case "Z" :
                match composant:
                    case "R" :
                        sub=symbols["R"f"{index}"]
                    case "C" :
                        sub=1/(symbols["C"f"{index}"]*p)
                    case "L" :
                        sub=symbols["L"f"{index}"]*p
            case "Y" :
                match composant :
                    case "R" :
                        sub=1/(symbols["R"f"{index}"])
                    case "C" :
                        sub=symbols["C"f"{index}"]*p
                    case "L" :
                        sub=1/(symbols["L"f"{index}"]*p)
            case _ :
                sub=symbols[symb]
        substitution.update({symb : sub})
    return substitution
# -----------------------------------------------------------------
# appliquer toutes les substitutions dans le dictionnaire substitutions
# -----------------------------------------------------------------
def apply_sub(expr,symbols,substitutions):
    for symb in symbols.keys():
        if symb in "pRLC" : continue
        expr = expr.subs(symbols[symb],substitutions[symb])
    return expr

# -----------------------------------------------------------------
# Ajouter un symbol au dictionnaire des symboles si on ajoute R1
# ZR1, YR1, R1 sont ajoutés
# -----------------------------------------------------------------
def add_symbol(symb,symbols):
    composant,index=symb
    for ZY in "ZY ":
        if ZY !=" ":
            symbols.update({f"{ZY}{symb}" : sp.Symbol(f"{ZY}_""{"f"{composant}_{index}""}" )})
        else:
            symbols.update({f"{symb}" : sp.Symbol(f"{composant}_{index}")})

# -----------------------------------------------------------------
# Construire le dictionnaires des symboles (p,R,L,C) sont de bases
# -----------------------------------------------------------------
def get_symbols(series,shunts):
    symbols={"p" : sp.Symbol("p"),"R":sp.Symbol("R"), "C":sp.Symbol("C"), "L":sp.Symbol("L")}
    cc={"R":0,"C":0,"L":0}
    for k, (serie,shunt) in enumerate(zip(series,shunts)):
        cc[serie]+=1
        add_symbol(serie+str(cc[serie]),symbols)
        if k < nquad - 1 : 
            cc[shunt]+=1
            add_symbol(shunt+str(cc[shunt]),symbols)
    for composant in shunts[-1]:
        cc[composant]+=1
        add_symbol(composant+str(cc[composant]),symbols)
    return symbols

# -----------------------------------------------------------------
# produire un document latex
# -----------------------------------------------------------------
def gentikz(page,series,shunts,symbols,composants):
    substitutions=get_substitutions(symbols)
    substitutions_equal=get_substitutions_equal(symbols)
    assert len(series)==len(shunts), f"la taille de series et shunts doit être la même {len(series)} {len(shunts)}"
    h=hash(tuple(series+shunts))
    out=[ltx("section*",f"Quadripole {composants} {page} {h:12x}")]
    out+=[begin("circuitikz","european resistors,straight voltages")]
    n=len(series)
    transfert_matrices=[]
    cc={"R":0,"C":0,"L":0}
    for k,(serie,shunt) in enumerate(zip(series,shunts)):
        cc[serie]+=1
        transfert_matrices.append(transfert_matrix(symbols[f"Z{serie}{cc[serie]}"],qtype="serie"))
        if k < n-1 :
            cc[shunt]+=1
            transfert_matrices.append(transfert_matrix(symbols[f"Z{shunt}{cc[shunt]}"],qtype="shunt"))
        out+=[quad_diff(n,k,cc,serie=serie,shunt=shunt,first=k==0,last=k==n-1)]
    out+=[end("circuitikz")]
    transfert_matrix_product = reduce(lambda x, y: x * y, transfert_matrices)
    out+=["\["]
    out+=["\prod_i T_i = "+ display_multi_dot_latex(transfert_matrices)]
    out+=["\]"]
    out+=["\["]
    out+=["T_{\mathrm{total}}="+display_matrix_latex(transfert_matrix_product)]
    out+=["\]"]
    add_admittance_out=[]
    for composant in shunts[-1]:
        cc[composant]+=1
        add_admittance_out.append(symbols[f"Y{composant}{cc[composant]}"])
    Ych=sum(add_admittance_out)
    Ych=apply_sub(Ych,symbols,substitutions)
    out+=["\["]
    out+=["Y_{CH}="+"+".join(f"Y_{sym}" for sym in shunts[-1])+"="+sp.latex(Ych)]
    out+=["\]"]
    expr=(transfert_matrix_product[0,0]+transfert_matrix_product[0,1]*Ych)
    expr=apply_sub(expr,symbols,substitutions)
    expr=sp.expand((1/expr))
    out+=["\["]
    out+=["H(p)="+sp.latex(sp.simplify(expr))]
    out+=["\]"]
    out+=[ltx("newline")]
    out+=[ltx("newline")]
    out+=[ltx("newline")]
    out+=[ltx("newline")]
    out+=[begin("circuitikz","european resistors,straight voltages")]
    for k,(serie,shunt) in enumerate(zip(series,shunts)):
        out+=[quad(n,k,serie=serie,shunt=shunt,first=k==0,last=k==n-1)]
    out+=[end("circuitikz")]
    expr=apply_sub(expr,symbols,substitutions_equal)
    out+=["\["]
    out+=["H(p)="+sp.latex(sp.simplify(expr))]
    out+=["\]"]
    out+=[ltx("clearpage")]
    return newlines(out)

#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------
def random_series_shunts(n,composants):
    series,shunts=[],[]
    for k in range(n):
        series.append(random.choice(composants))
        if k == n-1:
            if random.randint(0,1) :
                shunts.append(random.choice(composants)+random.choice(composants))
            else :
                shunts.append(random.choice(composants))
        else:
            shunts.append(random.choice(composants))
    return series,shunts

# -------------------------
# -----
def gen_main_latex_document(nquad,npages,composants):
    # latex header 
    out=[ltx("documentclass","article","tikz")]
    out+=[ltx("usepackage","amsmath")]
    out+=[ltx("usepackage","circuitikz")]
    out+=[begin("document")]

    deja_fait=set()
    page=1
    while page <= npages:
        print(f"{page:5}/{npages}",file=sys.stderr,end="\r")
        series,shunts=random_series_shunts(nquad,composants)
        # ---------------------------------------------------------------
        # on vérifie le hash de l'enchainement de composants
        # on veut tester que tous les composants sont bien représentés
        h=hash(tuple(series+shunts))
        s=set()
        for c in series+shunts: s |= set(c)
        if h in deja_fait or len(composants) > len(s) : continue
        #on ajouter à l'ensemble des hash déjà produit
        deja_fait.add(h)
        # ---------------------------------------------------------------
        # on génère les symboles pour le calcul symbolique sympy
        symbols=get_symbols(series,shunts)
        # on ajoute la page du quadrupole en tikz + formules
        out+=[gentikz(page,series,shunts,symbols,composants)]
        page+=1
    out+=[end("document")]
    return newlines(out)
    

if __name__=="__main__":
    assert len(sys.argv) != 3 , f"Usage: {sys.argv[0]} <nquad> <npages> <composants>"
    if len(sys.argv) == 0 :
        nquad,npages,composants=2,1,"RLC"
    else:
        nquad,npages,composants=int(sys.argv[1]),int(sys.argv[2]),sys.argv[3]

    print(gen_main_latex_document(nquad,npages,composants))
