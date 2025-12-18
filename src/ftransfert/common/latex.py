import numpy as np
# notation scientifique en LaTeX
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
def sci_latex_e(x, digits=1):
    return f"{x:.{digits}e}".replace("e", r"\mathrm{e}")
# -----------------------------------------------------------------
# join lines d'une liste
# -----------------------------------------------------------------
def concatenate(lines):
    return "".join(lines)
# -----------------------------------------------------------------
# applique \n à un ensemble de chaines dans une liste
# -----------------------------------------------------------------
def newlines(lines):
    return "\n".join(lines)
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

