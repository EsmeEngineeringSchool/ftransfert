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
from .string_ import strroot,strpoly 
from .utils import multiplicity

class Ftransfert():
    """
    Définition d'une Fonction de transfert (FT) :
        Une FT est définie par ces zéros et pôles (self.type='roots') ou des fonctions (lambda) pour ses
        polynômes au numérateur et dénominateur (self.type='function').
    """
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
        if zeros:
            self.zeros=zeros
            self.Czeros=[complex(*zero) for zero in zeros]
        else:
            self.zeros,self.Czeros=[],[]
        if poles:
            self.poles=poles
            self.Cpoles=[complex(*pole) for pole in poles]
        else:
            self.poles,self.Cpoles=[],[]
        # on vérifie si la FT est bien définie.
        # et on selectionne le type de la FT "functions" "roots" ou "polys"
        if len(self.Czeros) or len(self.Cpoles): self.type="roots"
        if callable(num) : self.type="functions"
        if isinstance(num,list) : self.type="polys"
        assert len(self.type) ,f"aucun type de fonction de tranfert n'est selectionné {self.type}"  

        # options for plotting phase
        self.phaseWrapping=False
        # riemann index,sign
        self.riemann=[0,-1]

        # la FT présente-elle des intégrateurs ?
        # deux tests selon le type de la
        if self.type == "functions" :
            self.integrators= self.den(0.0) == 0.0
        elif self.type == "roots" :
            if len(poles)>0 : self.integrators = not all(self.Cpoles).real!=0
        # obtenir la liste des w_i
        if self.type == "functions" :
            print("Pas possible pour l'instant d'obtenir les pulsations de ruptures à partir d'une fonction lambda")
            self.w_i=None
        elif self.type == "roots" :
            non_zeros=[abs(z) for z in self.Czeros if abs(z)>0.0]+\
                      [abs(p) for p in self.Cpoles if abs(p)>0.0]
            self.w_i=multiplicity(non_zeros)
        elif self.type == "polys" :
            print(f"polys -> z : {np.roots(self.num)}")
            print(f"polys -> p : {np.roots(self.den)}")
            non_zeros=[abs(z) for z in np.roots(self.num) if abs(z)>0.0]+\
                      [abs(p) for p in np.roots(self.den) if abs(p)>0.0]
            self.w_i=multiplicity(non_zeros)
        print(f"W_i {self.w_i}")
    # ------------------------------------------------------------------------------
    def eval(self,p,gain=None):
        """
        eval:
        Evaluation de la fonction de transfert associée à son type:
            Dans les deux cas retourne H(p),|H(p)|,arg{H(p)}

            si "functions" : retourne l'évaluation des deux fonctions en p.
            si "roots"    :
                                           (p-z1)(p-z2) ...
            retourne l'évaluation de   K -------------------
                                           (p-p1)(p-p2) ...
        """
        if not gain : gain=self.gain 
        match self.type :
            case "functions":
                if np.any(abs(p) == 0.0) and self.integrators : return
                h=gain*self.num(p)/self.den(p)
                return h,abs(h),np.arctan2(h.imag,h.real)
            case "roots" :
                h=complex(1,0)
                phase=0
                for zero in self.Czeros:
                    h*=(p-zero)
                    phase+=np.arctan2((p-zero).imag,(p-zero).real)
                for pole in self.Cpoles:
                    h/=(p-pole)
                    phase-=np.arctan2((p-pole).imag,(p-pole).real)
                h*=gain
                return h,abs(h),phase
            case "polys" :
                num=complex(0.0)
                for k,c in enumerate(self.num):
                    expo=len(self.num)-k-1
                    num+=c*p**expo
                den=complex(0.0)
                for k,c in enumerate(self.den):
                    expo=len(self.den)-k-1
                    den+=c*p**expo
                h=gain*num/den
                return h,np.abs(h),np.angle(h)

    # ------------------------------------------------------------------------------
    # retourne les parties réelles, imaginaires, le module et la phase de la
    # fonction de transfert complexe évaluée en w.
    # Un gain est donné en argument
    def harm_response(self,w,gain):
        h,mag,phase=self.eval(w,gain)
        # wrapping matlab like ... il faut calculer la phase à partir de l'évaluation complète
        if self.phaseWrapping :
            phase=np.zeros(h.shape)
            k=0
            for hi in h:
                phase[k]=self.atanN(hi.imag,hi.real)
                k+=1
        return h.real,h.imag,mag,phase
    # ------------------------------------------------------------------------------
    def latex(self,key="p"):
        if self.type == "functions": return "FT defined with lambda functions no latex available"
        match key :
            case "p" :
                return "\\boldsymbol{"f"{self.name}""(p)=\\dfrac{"\
                                      f"{strroot(self.Czeros,latex=True)}""}{"\
                                      f"{strroot(self.Cpoles,latex=True)}""}}"
            case "module":
                return "\phi(\omega)=\\arg{H(\jw)}"
            case "argument":
                return ""
            case "moduledB" :
                return ""
                
#    # --------------
#    #    phi(w)
#    # --------------
#    eqn_phase_reel="$$\phi(\omega)=\\arg{H(\jw)}="
#    if deriv_integ :
#        eqn_phase_reel+=str(int(classe*90))
#
#    for k,tau in enumerate(taus) :
#        if tau[1] != 0 :
#            if abs(tau[1]) != 1 :
#                if tau[1] > 0 :
#                    eqn_phase_reel+="+"+str(int(tau[1]))+"\\arctan{\\tau_"+str(k+1)+"\omega}"
#                else:
#                    eqn_phase_reel+=str(int(tau[1]))+"\\arctan{\\tau_"+str(k+1)+"\omega}"
#            else:
#                if tau[1] > 0 :
#                    eqn_phase_reel+="+\\arctan{\\tau_"+str(k+1)+"\omega}"
#                else:
#                    eqn_phase_reel+="-\\arctan{\\tau_"+str(k+1)+"\omega}"
#
#    eqn_phase_reel+="$$\n"
    def classe(self):
        match self.type :
            case "polys":
                for k,c in enumerate(self.den[::-1]):
                    if c != 0.0 :
                        return k
            case "roots":
                for p in self.poles:
                    pass


    def ordre(self):
        match self.type :
            case "polys":
                return len(self.den),len(self.num)
            case "roots":
                a=[abs(z) for z in self.Czeros if abs(z)>0.0]
                return 0,0
            case _:
                print("Impossible de déterminer l'ordre du polynome")
                return None,None

    def info(self):
        if self.verbeux >= 1 :
            print(52*'-')
            print(8*" "+"Infos")
            print(52*'-')
            print("Système       :")
            print(f"Gain                          : {self.gain}")
            if self.type == "functions" : return 
            print(f"classe                        = {self.classe()}")
            n,m=self.ordre()
            print(f"ordre global  (n)             = {n}")
            print(f"zeros         (m)             = {m}")
            print("m > n (non causal)") if m > n else print("m <= n (causal)")
            print()
            print("Sous-systèmes                  : ")
            print(f"tau/ordre                      : {self.w_i}")
            #print("intervalles pulsations         : ",intpuls)
            #print("valeurs particulières (calcul) : ",omegas)
            print()


    # ------------------------------------------------------------------------------
    def __repr__(self):
        match self.type :
            case "roots":
                return f'Ftranfert(zeros={self.zeros},poles={self.poles},gain={self.gain},name="{self.name}")'
            case "functions":
                return f'Ftranfert(num={type(self.num)},den={type(self.den)},gain={self.gain},name="{self.name}")'
            case "polys":
                return f'Ftranfert(num={self.num},den={self.den},gain={self.gain},name="{self.name}")'
    # ------------------------------------------------------------------------------
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

