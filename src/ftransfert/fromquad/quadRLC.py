import sys
import random
import sympy as sp
import math
from functools                    import reduce
from ftransfert.common.Ftransfert import Ftransfert
from ftransfert.common.utils      import nat2dB, rad2deg
from ftransfert.bode.tikz         import bode as bodetikz
from ftransfert.common.latex      import concatenate, newlines, macro, begin, end
from ftransfert.common.latex      import pmatrix as display_pmatrix 
from ftransfert.common.latex      import multi_dot as display_multi_dot

class SymbolsRLC():
    # quad est une instance de la classe Quad
    def __init__(self,quad):
        # -----------------------------------------------------------------
        # Construire le dictionnaires des symboles sympy 
        #  R_k,  C_k,  L_k ...
        # ZR_k, ZC_k, ZL_k ...
        # YR_k, YC_k, YL_k ...
        # avec (p,R,L,C) par défaut
        # -----------------------------------------------------------------
        self.symbols={"p" : sp.Symbol("p"),"R":sp.Symbol("R"), "C":sp.Symbol("C"), "L":sp.Symbol("L")}
        self.counting={"R":0,"C":0,"L":0}
        for k, (serie,shunt) in enumerate(zip(quad.series,quad.shunts)):
            self.counting[serie]+=1
            self.add_symbol(serie+str(self.counting[serie]))
            if k < quad.nquad - 1 : 
                self.counting[shunt]+=1
                self.add_symbol(shunt+str(self.counting[shunt]))
        for composant in quad.shunts[-1]:
            self.counting[composant]+=1
            self.add_symbol(composant+str(self.counting[composant]))
    # -----------------------------------------------------------------
    # Ajouter un symbol au dictionnaire des symboles si on ajoute R1
    # ZR1, YR1, R1 sont ajoutés
    # -----------------------------------------------------------------
    def add_symbol(self,symb):
        composant,index=symb
        for ZY in "ZY ":
            if ZY !=" ":
                self.symbols.update({f"{ZY}{symb}" : sp.Symbol(f"{ZY}_""{"f"{composant}_{index}""}" )})
            else:
                self.symbols.update({f"{symb}" : sp.Symbol(f"{composant}_{index}")})
    # ----------------------------------------------------------
    #  Retourne la substitution de base:
    #  ZRX -> RX
    #  ZCX -> 1/CXp
    #  ZLX -> LXp
    #  YRX -> 1/RX
    #  YCX -> CXp
    #  YLX -> 1/LXp
    #   RX -> RX
    #   CX -> CX
    #   LX -> LX
    # ----------------------------------------------------------
    def substitutions(self,equal=False):
        substitution={}
        p=self.symbols["p"]
        for symb in self.symbols.keys():
            if symb in "pRLC" : continue 
            if len(symb) == 2 : 
                ZY,index=symb
            elif len(symb) == 3 :
                ZY,composant,index=symb
            match ZY :
                case "Z" :
                    match composant:
                        case "R" :
                            sub =    self.symbols[f"R{index}"]      if not equal else self.symbols["R"]
                        case "C" :
                            sub = 1/(self.symbols["C"f"{index}"]*p) if not equal else 1/(self.symbols["C"]*p)
                        case "L" :
                            sub =    self.symbols["L"f"{index}"]*p  if not equal else self.symbols["L"]*p
                case "Y" :
                    match composant :
                        case "R" :
                            sub = 1/self.symbols[f"R{index}"]       if not equal else 1/self.symbols["R"]
                        case "C" :
                            sub =  (self.symbols["C"f"{index}"]*p)  if not equal else (self.symbols["C"]*p)
                        case "L" :
                            sub = 1/self.symbols["L"f"{index}"]*p   if not equal else 1/(self.symbols["L"]*p)
                case _ :
                    sub = self.symbols[symb] if not equal else self.symbols[symb[0]]
            substitution.update({symb : sub})
        return substitution
    # -----------------------------------------------------------------
    def gen_substitutions(self):
        self.subs=self.substitutions(False)
        self.subs_equal=self.substitutions(True)
    # -----------------------------------------------------------------
    # appliquer toutes les substitutions dans le dictionnaire substitutions
    # -----------------------------------------------------------------
    def apply_sub(self,expr,equal=False):
        for symb in self.symbols.keys():
            if symb in "pRLC" : continue
            if equal :
                expr = expr.subs(self.symbols[symb],self.subs[symb])
            else:
                expr = expr.subs(self.symbols[symb],self.subs_equal[symb])
        return expr
# -----------------------------------------------------------------
class Quad():
    def __init__(self,nquad,composants,series=None,shunts=None):
        self.nquad=nquad
        self.composants=composants
        self.series=series
        self.shunts=shunts
        self.substitutions=None
        self.substitutions_equal=None
        if self.series is not None and self.shunts is not None :
            self.calc()
    # -----------------------------------------------------------------
    def gen_symbols(self):
        self.symbolsRLC = SymbolsRLC(self)
    # -----------------------------------------------------------------
    def get_hash(self):
        if self.series == None or self.shunts == None : return 
        return hash(tuple(self.series+self.shunts))
    # -----------------------------------------------------------------
    def get_poly(self):
        num_poly = sp.Poly(sp.expand(self.sp_tfnum), self.symbolsRLC.symbols['p']).all_coeffs()
        den_poly = sp.Poly(sp.expand(self.sp_tfden), self.symbolsRLC.symbols['p']).all_coeffs()
        return num_poly,den_poly
    # -----------------------------------------------------------------
    def get_ftransfert_from_RLC(self,R,C,L,name="H"):
        num_poly,den_poly=self.get_poly()
        evaluation={self.symbolsRLC.symbols['R']: R, \
                    self.symbolsRLC.symbols['C']: C, \
                    self.symbolsRLC.symbols['L']: L}
        evalnum=[float(c.evalf(subs=evaluation)) for c in num_poly]
        evalden=[float(c.evalf(subs=evaluation)) for c in den_poly]
        return Ftransfert(num=evalnum,den=evalden,gain=1,name="H")

    # -----------------------------------------------------------------
    def calc(self):
        # ---------------------------------------------------------------
        # on génère les symboles pour le calcul symbolique sympy
        self.gen_symbols()
        self.symbolsRLC.gen_substitutions()
        # Calcul de la matrice de transfert, admittance de sortie et fonction de transfert associé
        self.gen_transfert_matrices()
        self.gen_admittance_out()
        self.gen_sp_transfert_function()
    # -----------------------------------------------------------------
    def random(self):
        series,shunts=[],[]
        for k in range(self.nquad):
            series.append(random.choice(self.composants))
            if k == self.nquad-1:
                if random.randint(0,1) :
                    shunts.append(random.choice(self.composants)+random.choice(self.composants))
                else :
                    shunts.append(random.choice(self.composants))
            else:
                shunts.append(random.choice(self.composants))
        self.series=series
        self.shunts=shunts
        self.calc()
    # --------------------------------------------------------------------------
    def get_counting_components_without_Ych(self):
        cc={"R":0,"C":0,"L":0}
        n=len(self.series)
        for k,(serie,shunt) in enumerate(zip(self.series,self.shunts)):
            cc[serie]+=1
            if k <n -1 : cc[shunt]+=1
        return cc
    # --------------------------------------------------------------------------
    def gen_sp_transfert_function(self):
        self.sp_tfunction=(self.sp_tmatrix[0,0]+self.sp_tmatrix[0,1]*self.sp_Ych)
        self.sp_tfunction=self.symbolsRLC.apply_sub(self.sp_tfunction,equal=False)
        self.sp_tfunction=sp.expand((1/self.sp_tfunction))
        self.sp_tfnum, self.sp_tfden = sp.together(self.sp_tfunction).as_numer_denom()
    # --------------------------------------------------------------------------
    def gen_transfert_matrices(self):
        n=len(self.series)
        self.tmatrices=[]
        cc={"R":0,"C":0,"L":0}
        for k,(serie,shunt) in enumerate(zip(self.series,self.shunts)):
            cc[serie]+=1
            self.tmatrices.append(self.transfert_matrix(self.symbolsRLC.symbols[f"Z{serie}{cc[serie]}"],qtype="serie"))
            if k < n-1 :
                cc[shunt]+=1
                self.tmatrices.append(self.transfert_matrix(self.symbolsRLC.symbols[f"Z{shunt}{cc[shunt]}"],qtype="shunt"))
        self.sp_tmatrix = reduce(lambda x, y: x * y, self.tmatrices)

    # --------------------------------------------------------------------------
    def gen_admittance_out(self):
        add_admittance_out=[]
        cc=self.get_counting_components_without_Ych()
        for composant in self.shunts[-1]:
            cc[composant]+=1
            add_admittance_out.append(self.symbolsRLC.symbols[f"Y{composant}{cc[composant]}"])
        self.sp_Ych=sum(add_admittance_out)
    # --------------------------------------------------------------------------
    def __str__(self):
        if self.series is None : return "None"
        out=["*" if k in [0,4] else " " for k in range(5)]
        for k,(serie,shunt) in enumerate(zip(self.series,self.shunts)):
            if len(shunt) < 2 :
                out[0]+=f" ---- {serie} ---- *"
                out[1]+=f"             |"
                out[2]+=f"             {shunt}"
                out[3]+=f"             |"
                out[4]+=f" ----------- *"
            else:
                out[0]+=f" ---- {serie} ---- * ---- *"
                out[1]+=      f"             |      |"
                out[2]+=      f"             {shunt[0]}      {shunt[1]}"
                out[3]+=      f"             |      |"
                out[4]+=      f" ----------- * ---- *"
        return newlines(out+[""])
    # --------------------------------------------------------------------------
    # tikz Quadripole (tous les composants sont identiques)
    #   * -- SERIE -- * -- * -- SERIE -- * ----- *
    #                 |                    |     |
    #               SHUNT                SHUNT  SHUNT 
    #                 |                    |     |
    #   * ----------- * ---- * ----------- * --- *
    # si dernier quadripole SHUNT peut être doublé 
    # --------------------------------------------------------------------------
    def tikz(self,index,serie="R",shunt="R",first=False,last=False,):
        e,s=1,2
        out =[begin("scope","shift={("f"{4*index}"",0)}")]
        out+=[macro("draw")]
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
    def tikz_diff(self,index,counting,serie="R",shunt="R",first=False,last=False):
        e,s=1,2
        out=[begin("scope","shift={("f"{4*index}"",0)}")]
        out+=[macro("draw")]
        out+=["(0,0) to [short, *-] (4,0)"]
        if last : 
            if serie == shunt :
                out+=["(0,3) to ["f"{serie[0]}=${serie[0]}_{counting[serie]}$""] (4,3)"]
            else:
                out+=["(0,3) to ["f"{serie[0]}=${serie[0]}_{counting[serie]}$""] (4,3)"]
            out+=["(4,0) to ["f"{shunt[0]}=${shunt[0]}_{counting[shunt[0]]+1}$"",*-*] (4,3)"]
            if len(shunt)>1 :
                out+=["(4,0) to [short, *-] (5.5,0)"]
                out+=["(4,3) to [short, *-] (5.5,3)"]
                if shunt[0] == shunt[1] :
                    out+=["(5.5,0) to ["f"{shunt[1]}=${shunt[1]}_{counting[shunt[1]]+2}$"",*-*] (5.5,3)"]
                else:
                    out+=["(5.5,0) to ["f"{shunt[1]}=${shunt[1]}_{counting[shunt[1]]+1}$"",*-*] (5.5,3)"]
                out+=["(6.2,0) to [open,v_>=$V_{"f"{s}""}$] (6.2,3)"]
            else:
                out+=["(5,0) to [open,v_>=$V_{"f"{s}""}$] (5,3)"]
            out+=["(3,3) to [short, -* ,i=$I_{"f"{s}""}$] (4,3)"]
        else:
            if serie == shunt :
                out+=["(0,3) to ["f"{serie[0]}=${serie[0]}_{counting[serie]-1}$""] (4,3)"]
            else:
                out+=["(0,3) to ["f"{serie[0]}=${serie[0]}_{counting[serie]}$""] (4,3)"]
            out+=["(4,0) to ["f"{shunt[0]}=${shunt[0]}_{counting[shunt[0]]}$"",*-*] (4,3)"]
        if first :
            out+=["(0,3) to [short, *- ,i=$I_{"f"{e}""}$] (1,3)"]
            out+=["(0,0) to [open,v^>=$V_{"f"{e}""}$] (0,3)"]
        out+=[";"]
        out+=[end("scope")]
        return newlines(out)
    # -----------------------------------------------------------------
    # Create a tranfert matrix serie ou shunt  
    # -----------------------------------------------------------------
    def transfert_matrix(self,Z,qtype="serie"):
        match qtype :
            case "serie" :
                return sp.Matrix([[1,Z],[0,1]])
            case "shunt" :
                return sp.Matrix([[1,0],[1/Z,1]])
    # -----------------------------------------------------------------
    # produire un document latex
    # -----------------------------------------------------------------
    def genpage(self,page):
        assert len(self.series)==len(self.shunts), f"la taille de series et shunts doit être la même {len(series)} {len(shunts)}"
        out=[macro("section*",f"Quadripole {composants} {page} {self.get_hash():12x}")]
        out+=[begin("center")]
        out+=[begin("circuitikz","european resistors,straight voltages")]
        n=len(self.series)
        cc={"R":0,"C":0,"L":0}
        for k,(serie,shunt) in enumerate(zip(self.series,self.shunts)):
            cc[serie]+=1
            if k < n-1 : cc[shunt]+=1
            out+=[self.tikz_diff(k,cc,serie=serie,shunt=shunt,first=k==0,last=k==n-1)]
        out+=[end("circuitikz")]
        out+=[end("center")]
        out+=["\["]
        out+=["\prod_i T_i = "+ display_multi_dot(self.tmatrices)]
        out+=["\]"]
        out+=["\["]
        out+=["T_{\mathrm{total}}="+display_pmatrix(self.sp_tmatrix)]
        out+=["\]"]
        out+=["\["]
        out+=["Y_{CH}="+"+".join(f"Y_{sym}" for sym in self.shunts[-1])+"="+sp.latex(self.sp_Ych)]
        out+=["\]"]
        out+=["\["]
        out+=["H(p)="+sp.latex(sp.simplify(self.sp_tfunction))]
        out+=["\]"]
        out+=[macro("newline")]
        out+=[macro("newline")]
        out+=[macro("newline")]
        out+=[macro("newline")]
        out+=[begin("center")]
        out+=[begin("circuitikz","european resistors,straight voltages")]
        for k,(serie,shunt) in enumerate(zip(self.series,self.shunts)):
            out+=[self.tikz(k,serie=serie,shunt=shunt,first=k==0,last=k==n-1)]
        out+=[end("circuitikz")]
        out+=[end("center")]
        expr=self.symbolsRLC.apply_sub(self.sp_tfunction,equal=True)
        out+=["\["]
        out+=["H(p)="+sp.latex(sp.simplify(expr))]
        out+=["\]"]
        return newlines(out)

# -----------------------------------------------------------------------------
def gen_main_latex_document(nquad,npages,composants):
    out=[macro("documentclass","article","tikz")]
    out+=[macro("usepackage","geometry")]
    out+=[macro("geometry","paperwidth=21cm,\npaperheight=29.7cm,\nmargin=1cm")]
    out+=[macro("usepackage","amsmath")]
    out+=[macro("usepackage","mathfmv")]
    out+=[macro("usepackage","circuitikz")]
    out+=[macro("usepackage","siunitx")]
    out+=[macro("usepackage","pgf")]
    out+=[macro("usepackage","tikz")]
    out+=[macro("usepackage","pgfplots")]
    out+=[macro("pgfplotsset","compat=1.18")]
    out+=[begin("document")]
    deja_fait=set()
    page=1
    while page <= npages:
        print(f"{page:5}/{npages}",file=sys.stderr,end="\r")
        # random_quad_object
        quad=Quad(nquad,composants)
        quad.random()
        #series,shunts = random_series_shunts(nquad,composants)
        # ---------------------------------------------------------------
        # on vérifie le hash de l'enchainement de composants
        # on veut tester que tous les composants sont bien représentés
        s=set()
        for c in quad.series+quad.shunts: s |= set(c)
        if quad.get_hash() in deja_fait or len(composants) > len(s) : continue
        # ---------------------------------------------------------------
        #on ajouter à l'ensemble des hash déjà produit
        deja_fait.add(quad.get_hash())
        # ---------------------------------------------------------------
        # on ajoute la page du quadrupole en tikz + formules
        tikz = quad.genpage(page)
        out+=[tikz]
        num_poly = sp.Poly(sp.expand(quad.sp_tfnum), quad.symbolsRLC.symbols['p']).all_coeffs()
        den_poly = sp.Poly(sp.expand(quad.sp_tfden), quad.symbolsRLC.symbols['p']).all_coeffs()
        gain=1
        R,C,L=1000,1e-6,0.001
        evaluation={ quad.symbolsRLC.symbols['R']: R, quad.symbolsRLC.symbols['C']: C, quad.symbolsRLC.symbols['L']:L}
        evalnum=[float(c.evalf(subs=evaluation)) for c in num_poly]
        evalden=[float(c.evalf(subs=evaluation)) for c in den_poly]
        H=Ftransfert(num=evalnum,den=evalden,gain=gain,name="H")
        H.info()
        print(H)
        out+=["\["]
        out+=["R=\SI{"f"{R}""}""{\ohm}"]
        out+=["\]"]
        out+=["\["]
        out+=["C=\SI{"f"{C}""}""{\\farad}"]
        out+=["\]"]
        out+=["\["]
        out+=["L=\SI{"f"{L}""}""{\henry}"]
        out+=["\]"]
        out+=[macro("clearpage")]
        # estimation automatique des intervalles xlim,y1lim,y2lim
        # à partir des valeurs de R,C,L
        w=[R/L,1/(R*C),1/(L*C)**0.5] 
        xlim=(10**round(math.log10(min(w)/1000)),10**round(math.log10(1000*max(w))))
        g,p=[],[]
        for wi in w:
            pow10_w = 10**round(math.log10(wi/10))
            _,gw,pw=H.eval(pow10_w*1j)
            g.append(nat2dB(gw))
            p.append(rad2deg(pw))
        _,gm,pm=H.eval(1j*(xlim[1]*xlim[0])**0.5)
        g.append(nat2dB(gm))
        p.append(rad2deg(pm))
        g.sort()
        p.sort()
        g0f,g1f=math.floor(g[0]/10)*10-20,math.ceil(g[-1]/10)*10+40
        p0f,p1f=math.floor(p[0]/90)*90,math.ceil(p[-1]/90)*90
        out+=[bodetikz(H,filename=None,latex_document=False,xlim=xlim,y1lim=(g0f,g1f),y2lim=(p0f,p1f))]
        page+=1
    out+=[end("document")]
    return newlines(out)
    
# -----------------------------------------------------------------------------
if __name__=="__main__":
    assert len(sys.argv) != 3 , f"Usage: {sys.argv[0]} <nquad> <npages> <composants>"
    if len(sys.argv) == 0 :
        nquad,npages,composants,filename=2,1,"RLC","test.tex"
    else:
        nquad,npages,composants,filename=int(sys.argv[1]),int(sys.argv[2]),sys.argv[3],sys.argv[4]
    with open(filename,"w") as f:
        print(gen_main_latex_document(nquad,npages,composants),file=f)
