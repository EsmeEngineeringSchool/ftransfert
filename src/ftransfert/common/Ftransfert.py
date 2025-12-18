# -----------------------------------------------------------------------------
# ftransfert class 
# author : fmv
# date : 2025 
# description :
#    Ce script permet de définir la classe fonction de transfert utile
#    à différentes modules de tracés de réponses harmoniques avec matplotlib
#    et PGF/Tikz
#    Born Again d'un module du même nom des années 2019-2020 (qui était buggé!!).
import numpy as np
import sympy as sp
from .string_ import strroot, strpoly, signstr, newlines
from .utils import multiplicity, factorize, eval_poly, eval_poly_symbol, nat2dB, rad2deg, atanN,TWO_PI

class Ftransfert():
    """
    Définition d'une Fonction de transfert (FT) :
        Une FT est définie par ces zéros et pôles (self.type='roots') ou des fonctions (lambda) pour ses
        polynômes au numérateur et dénominateur (self.type='function').
    """
    # -----------------------------------------------------------------------------------
    def __init__(self,zeros=None,poles=None,num=None,den=None,gain=1,title='',name="F",verbeux=1):
        self.gain=gain       # gain de la FT
        self.num=num         # polynôme au numérateur
        self.den=den         # polynôme au dénominateur
        self.name=name       # nom de la FT
        self.title=title     # information supplémentaire à ajouter au titre des diagrammes
        self.verbeux=verbeux # verbose
        if num and den :
            assert isinstance(self.num,list) and isinstance(self.den,list) or callable(num) and callable(den),\
                   "num et den doivent être des listes (de coeff. polynomes) ou des fonctions (callable)" 
        self.Czeros,self.Cpoles=[],[]
        if zeros:
            self.zeros=zeros
            self.Czeros=[complex(*zero) for zero in zeros]
        if poles:
            self.poles=poles
            self.Cpoles=[complex(*pole) for pole in poles]
        # on vérifie si la FT est bien définie.
        # et on selectionne le type de la FT "functions" "roots" ou "polys"
        if len(self.Czeros) or len(self.Cpoles): self.type="roots"
        if callable(num) : self.type="functions"
        if isinstance(num,list) : self.type="polys"
        assert len(self.type) ,f"aucun type de fonction de tranfert n'est selectionné {self.type}"  

        # classe 
        self.classe=self.get_classe()

        match self.type :
            case "functions":
                # intégrateurs
                self.integrators= self.den(0.0) == 0.0
                # w_i (pulsations de ruptures)
                print("Pas possible pour l'instant d'obtenir les pulsations de ruptures à partir d'une fonction lambda")
                self.w_i=None
            case "polys" :
                self.num=factorize(self.num)
                self.den=factorize(self.den)
                print("debug",self.num,self.den)
                # intégrateurs
                self.integrators= eval_poly(self.den,0.0) ==0.0
                # zeros et poles
                #self.Czeros=np.roots(np.array(self.num,dtype=complex))
                #self.Cpoles=np.roots(np.array(self.den,dtype=complex))
                self.Czeros=[complex(x) for x in np.roots(self.num)]
                self.Cpoles=[complex(x) for x in np.roots(self.den)]
                # w_i (pulsations de ruptures)
                self.w_i=[]
                non_zeros=[abs(z) for z in self.Czeros if abs(z)>0.0]
                self.w_i+=multiplicity(non_zeros,1.0)
                non_zeros=[abs(p) for p in self.Cpoles if abs(p)>0.0]
                self.w_i+=multiplicity(non_zeros,-1.0)
                self.w_i.sort(key=lambda x: x[0])
                # ------------------------------
                # gain statique 
                gnum,gden=1,1
                for z in self.Czeros :
                    if abs(z) > 0.0 : gnum/=abs(z)
                for p in self.Cpoles :
                    if abs(p) > 0.0 : gden/=abs(p)
                self.gain_static=self.gain*gnum/gden
                # ------------------------------
            case "roots" :
                # intégrateurs
                if len(poles)>0 : self.integrators = not all(self.Cpoles).real!=0
                # w_i (pulsations de ruptures)
                self.w_i=[]
                non_zeros=[abs(z) for z in self.Czeros if abs(z)>0.0]
                self.w_i+=multiplicity(non_zeros,1.0)
                non_zeros=[abs(p) for p in self.Cpoles if abs(p)>0.0]
                self.w_i+=multiplicity(non_zeros,-1.0)
                self.w_i.sort(key=lambda x: x[0])
                # ------------------------------
                # gain statique 
                gnum,gden=1,1
                for z in self.Czeros :
                    if abs(z) > 0.0 : gnum/=abs(z)
                for p in self.Cpoles :
                    if abs(p) > 0.0 : gden/=abs(p)
                self.gain_static=self.gain*gnum/gden
        # ------------------------------
        
        # ------------------------------
        # ENCORE UTILE ?
        # options for plotting phase
        self.phaseWrapping=True
        # riemann index,sign
        self.riemann=[0,-1]
        # ------------------------------

    # ------------------------------------------------------------------------------
    def eval(self,p,gain=1):
        """
        eval:
        Evaluation de la fonction de transfert associée à son type:
            Dans les deux cas retourne H(p),|H(p)|,arg{H(p)}

            si "functions" : retourne l'évaluation des deux fonctions en p.
            si "roots"    :
                                          p^i (p-z1)(p-z2) ...
            retourne l'évaluation de   K -------------------
                                          p^d (p-p1)(p-p2) ...
        """
        match self.type :
            case "functions":
                if np.any(abs(p) == 0.0) and self.integrators : return
                h=gain*self.num(p)/self.den(p)
                return h,abs(h),np.arctan2(h.imag,h.real)
            case "roots" :
                h=complex(1,0)
                phase=0.
                for zero in self.Czeros:
                    if abs(zero) == 0.0 :continue
                    h*=(p-zero)
                    phase+=np.arctan2((p-zero).imag,(p-zero).real)
                for pole in self.Cpoles:
                    if abs(pole) == 0.0 :continue
                    h/=(p-pole)
                    phase-=np.arctan2((p-pole).imag,(p-pole).real)
                i,d = self.classe
                for k in range(i) : 
                    h/=p
                    phase-=np.arctan2(p.imag,p.real)
                for k in range(d) : 
                    h*=p
                    phase+=np.arctan2(p.imag,p.real)
                h*=gain
                h*=self.gain_static
                return h,abs(h),phase
            case "polys" :
                num,den=eval_poly(self.num,p),eval_poly(self.den,p)
                h=gain*num/den
                h*=self.gain
                return h,np.abs(h),np.angle(h)
    # ------------------------------------------------------------------------------
    # retourne les parties réelles, imaginaires, le module et la phase de la
    # fonction de transfert complexe évaluée en w.
    # Un gain est donné en argument
    def harmonic_response(self,w,gain):
        h,mag,phase=self.eval(w,gain)
        # wrapping matlab like ... il faut calculer la phase à partir de l'évaluation complète
        if self.phaseWrapping :
            phase=np.zeros(h.shape)
            k=0
            for hi in h:
                phase[k]=atanN(self,hi.imag,hi.real)
                k+=1
        return h.real,h.imag,mag,phase
    # ------------------------------------------------------------------------------------
    # retourne la représentation addplot de la fonction de transfert
    def addplot(self,key):
        match key :
            case "moduledB" :
                num,den="",""
                i,d=self.classe
                si=f"-{20*i}*log10(x)" if i != 0 else ""
                sd=f"+{20*d}*log10(x)" if d != 0 else ""
                den+=f"{si}"
                num+=f"{sd}"
                for k,z in enumerate(self.Czeros):
                    if abs(z) == 0.0 : continue 
                    num+=f"+10*log10({z.real**2}+(x+({z.imag}))*(x+({z.imag})))"
                for k,p in enumerate(self.Cpoles):
                    if abs(p) == 0.0 : continue 
                    den+=f"-10*log10({p.real**2}+(x+({p.imag}))*(x+({p.imag})))"
                return f"{20*np.log10(self.gain_static)}"f"{num}"f"{den}"
            case "argument":
                i,d=self.classe
                out=""
                if d-i != 0 :
                    out+=f"{int((d-i)*90)}"
                for k,w in enumerate(self.w_i):
                    m=(int(w[1]) if abs(w[1]) !=1 else signstr(w[1]))
                    out+=f"+({int(w[1])})*atan2(x/{w[0]},1)"
                return out
    # ------------------------------------------------------------------------------------
    # retourne la représentation math display de LaTeX
    def latex(self,key="p"):
        if self.type == "functions": return "FT defined with lambda functions no latex available"
        match key :
            case "p" :
                match self.type :
                    case "roots":
                        if len(strroot(self.Cpoles,latex=True)):
                            return "\\boldsymbol{"f"{self.name}""(p)="f"{self.gain}""\\dfrac{"\
                                                  f"{strroot(self.Czeros,latex=True)}""}{"\
                                                  f"{strroot(self.Cpoles,latex=True)}""}}"
                        else:
                            return "\\boldsymbol{"f"{self.name}""(p)="f"{self.gain}"\
                                                  f"{strroot(self.Czeros,latex=True)}""}"

                    case "polys":
                        gain_shown=self.gain if self.gain !=1 else ""
                        return "\\boldsymbol{"f"{self.name}""(p)="f"{gain_shown}""\\dfrac{"\
                                              f"{strpoly(self.num,latex=True)}""}{"\
                                              f"{strpoly(self.den,latex=True)}""}}"
            case "moduledB" :
                num,den="",""
                i,d=self.classe
                si=f"-({20*i})\\log\omega" if i != 0 else ""
                sd=f"+({20*d})\\log\omega" if d != 0 else ""
                den+=f"{si}"
                num+=f"{sd}"
                for k,w in enumerate(self.w_i):
                    re="1+"
                    im="\\left(\\frac{\omega}{\omega_"f"{k+1}""}\\right)^2"
                    if w[1] < 0:
                        den+=f"{int(10*w[1])}""\\log{\\left("f"{re}{im}""\\right)}"
                    else:
                        num+=f"+{int(10*w[1])}""\\log{\\left("f"{re}{im}""\\right)}"

                return "G_{dB}(\omega)="f"{int(20*np.log10(self.gain_static))}"f"{num}"f"{den}" 
            case "module":
                num,den="{","{"
                if self.gain_static != 1 : num+=f"{int(self.gain_static)}""\left("
                if self.type == "polys" :
                    w=sp.Symbol(r"\omega")
                    num+=sp.latex(sp.nsimplify(eval_poly_symbol(self.num,w*sp.I).expand()),imaginary_unit="j")
                    den+=sp.latex(sp.nsimplify(eval_poly_symbol(self.den,w*sp.I).expand()),imaginary_unit="j")
                if self.type == "roots":
                    i,d=self.classe
                    powi=f"^{i}"       if i  > 1 else ""
                    powd=f"^{d}"       if d  > 1 else ""
                    si=f"\omega{powi}" if i != 0 else ""
                    sd=f"\omega{powd}" if i != 0 else ""
                    den+=f"{si}"
                    num+=f"{sd}"
                    for k,w in enumerate(self.w_i):
                        for m in range(int(abs(w[1]))) :
                            re="1+"
                            im="\\left(\\frac{\omega}{\omega_"f"{k+1}""}\\right)^2"
                            if w[1] < 0 :
                                den+="\sqrt{"f"{re}{im}""}"
                            else :
                                num+="\sqrt{"f"{re}{im}""}"
                num+="\\right)}"
                den+="}"
                if len(den) > 2 :
                    return f"G(\omega)=|H(\jw)|=\dfrac{num}{den}"
                else:
                    return f"G(\omega)=|H(\jw)|={num}"
            case "argument":
                i,d=self.classe
                out="\phi(\omega)=\\arg{H(\jw)}="
                if d-i != 0 :
                    out+=f"{int((d-i)*90)}"
                for k,w in enumerate(self.w_i):
                    m=(int(w[1]) if abs(w[1]) !=1 else signstr(w[1]))
                    out+=f"{m}""\\arctan{\left(\\frac{\omega}{\omega_"f"{k+1}""}\\right)}"
                return out
    def isin_tol(self,x, iterable, rtol=1e-9, atol=0.0):
        print("debug isin_tol",type(iterable))
        return any(np.isclose(x, y, rtol=rtol, atol=atol) for y in iterable)
    # ------------------------------------------------------------------------------------
    def tablatex(self,**kwargs):
        class nf(float):
            def __repr__(self):
                return f'{self:12.5f}'
        ws=kwargs.get('ws',None)
        winput=isinstance(ws,np.ndarray)
        wlim=kwargs.get('wlim', (1e-2,1e2))
        n=kwargs.get('n',11)
        # array of pulsations
        if not winput :
            ws_real = np.unique(np.round( np.concatenate((
                         np.logspace(np.log10(wlim[0]), np.log10(wlim[1]), n),
                         np.array([w[0] for w in self.w_i])
                      )),decimals=6))
            ws=1j*np.sort(ws_real)
        response=self.harmonic_response(ws,self.gain)
        out=["\\begin{center}"]
        out+=["\\begin{tabular}{ccc}"]
        out+=["\\hline"]
        out+=["$\omega$ (\si{\\radian\per\second}) & Gain (\si{\decibel}) & Phase (\si{\degree})\\\\"]
        out+=["\\hline"]
        for w,m,p in zip(ws,response[2],response[3]):
            print("debug",abs(w),list(w_i[0] for w_i in self.w_i))
            if self.isin_tol(abs(w), (w_i[0] for w_i in self.w_i)) :
                out+=["\\textbf{"+str(nf(abs(w)))+"} & \\textbf{"+str(nf(nat2dB(m)))+"} & \\textbf{"+str(nf(rad2deg(p)))+"}\\\\"]
            else:
                out+=[str(nf(abs(w)))+" & "+str(nf(nat2dB(m)))+" & "+str(nf(rad2deg(p)))+"\\\\"]
            out+=["\\hline"]
        out+=["\end{tabular}"]
        out+=["\\end{center}"]
        return newlines(out)

    #i,d # classe des intégrateurs et dérivateurs
    def get_classe(self):
        match self.type :
            case "functions":
                print(f"Classe n'est pas accessible avec le type 'functions'")
            case "polys":
                i = next((k for k, c in enumerate(reversed(self.den)) if c != 0.0), None)
                d = next((k for k, c in enumerate(reversed(self.num)) if c != 0.0), None)
                return i,d
            case "roots":
                i = sum([1 for z in self.Cpoles if abs(z) == 0.0])
                d = sum([1 for p in self.Czeros if abs(p) == 0.0])
                return i,d

    # n,m 
    def ordre(self):
        match self.type :
            case "polys":
                return len(self.den)-1,len(self.num)-1
            case "roots":
                return len(self.Cpoles),len(self.Czeros)
            case _:
                print("Impossible de déterminer l'ordre du polynome")
                return None,None
    # 
    def info(self):
        if self.verbeux >= 1 :
            print(52*'-')
            print(8*" "+"Ftransfert Infos")
            print(52*'-')
            print(f"Système       (type:{self.type})")
            print(f"Gain                          : {self.gain}")
            print(f"Gain (static)                 : {self.gain_static}")
            if self.type == "functions" : return 
            i,d=self.classe
            print(f"nombre d'intégrateurs (i)     = {i}")
            print(f"nombre de dérivateurs (d)     = {d}")
            n,m=self.ordre()
            print(f"poles         (n)             = {n} {self.Cpoles}")
            print(f"zeros         (m)             = {m} {self.Czeros}")
            print("m > n (non causal)") if m > n else print("m <= n (causal)")
            print()
            print( "Sous-systèmes                 : ")
            print(f"pulsations, multiplicité      : {', '.join(f'({w:5.2f}, {m})' for w, m in self.w_i)}")
            #print("intervalles pulsations        : ",intpuls)
            #print("valeurs particulières (calcul): ",omegas)
            print()
    # ------------------------------------------------------------------------------------
    def __repr__(self):
        match self.type :
            case "roots":
                return f'Ftranfert(zeros={self.Czeros},poles={self.Cpoles},gain={self.gain},name="{self.name}")'
            case "functions":
                return f'Ftranfert(num={type(self.num)},den={type(self.den)},gain={self.gain},name="{self.name}")'
            case "polys":
                return f'Ftranfert(num={self.num},den={self.den},gain={self.gain},name="{self.name}")'
    # ------------------------------------------------------------------------------------
    def __str__(self):
        """
                          (p-z1)(p-z2)(p-z3)...
            F(p) = gain  ------------------------
                          (p-p1)(p-p2)(p-p3)...
        """
        match self.type :
            case "functions": 
                return "FT defined with lambda functions no str representation"
            case "roots":
                return self.strfrac(self.type)
            case "polys":
                return self.strfrac(self.type)
    # ------------------------------------------------------------------------------------
    def strfrac(self,mode):
        if mode == "roots":
            outnum=strroot(self.Czeros)
            outden=strroot(self.Cpoles)
        elif mode == "polys":
            outnum=strpoly(self.num)
            outden=strpoly(self.den)
        else:
            return
        outname=f"{self.name}(p) = "
        if len(outnum) == 0 :
            outnum=str(self.gain)
            outgain=''
        else:
            outgain= str(self.gain)+' ' if self.gain !=1 else ''
        lz,lp=len(outnum),len(outden)
        diff=(lz-lp)//2
        if diff>0:
            dz,dp=0,diff
        else:
            dz,dp=-diff,0
        spacenum=len(outname)+len(outgain)+dz
        spaceden=len(outname)+len(outgain)+dp
        dashed=max(len(outnum),len(outden))
        out='\n'
        if len(outden) !=0 :
            out+=spacenum*' '+outnum+'\n'
            out+=outname+outgain+dashed*'-'+'\n'
        else:
            out+=outname+outgain+outnum
        out+=spaceden*' '+outden+'\n'
        return out

