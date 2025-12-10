# -----------------------------------------------------------------------------
# ftransfert class 
# author : fmv
# date : 2025 
# description :
#    Ce script permet de définir la classe fonction de transfert utile
#    à différentes modules de tracés de réponses harmoniques avec matplotlib
#    et PGF/Tikz
#    Born Again d'un module du même nom des années 2019-2020.
import numpy as np
from .string_ import strroot 

class Ftransfert():
    """
    Définition d'une Fonction de transfert (FT) :
        Une FT est définie par ces zéros et pôles (self.type='roots') ou des fonctions (lambda) pour ses
        polynômes au numérateur et dénominateur (self.type='function').
    """
    def __init__(self,zeros=None,poles=None,num=None,den=None,gain=1,title='',name="F",verbeux=1):
        self.gain=gain       # gain statique de la FT
        self.num=num         # polynôme au numérateur
        self.den=den         # polynôme au dénominateur
        self.name=name       # nom de la FT
        self.title=title     # information supplémentaire à ajouter au titre des diagrammes
        self.verbeux=verbeux # verbose
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
        # et on selectionne le type de la FT "function" ou "roots"
        defOK=(self.Czeros!=[] or self.Cpoles!=[]) or (self.num!=None and self.den!=None)
        if defOK:
            if self.num!=None or self.den!=None :
                self.type="function"
                self.Czeros=[]
                self.Cpoles=[]
            else:
                self.type="roots"
        else:
            self.type=None
            print('Erreur dans la définition de la fonction de transfert')

        # options for plotting phase
        self.phaseWrapping=False
        # riemann index,sign
        self.riemann=[0,-1]

        # la FT présente-elle des intégrateurs ?
        # deux tests selon le type de la
        if self.type == "function" :
            self.integrators= self.den(0.0) == 0.0
        elif self.type == "roots" :
            if len(poles)>0 : self.integrators = not all(self.Cpoles).real!=0
    # ------------------------------------------------------------------------------
    def eval(self,p,gain):
        """
        eval:
        Evaluation de la fonction de transfert associée à son type:
            Dans les deux cas retourne H(p),|H(p)|,arg{H(p)}

            si "function" : retourne l'évaluation des deux fonctions en p.
            si "roots"    :
                                           (p-z1)(p-z2) ...
            retourne l'évaluation de   K -------------------
                                           (p-p1)(p-p2) ...
        """
        match self.type :
            case "function":
                if np.any(abs(p) == 0.0) and self.integrators : return
                h=gain*self.num(p)/self.den(p)
                return h,abs(h),np.arctan2(h.imag,h.real)
            case "roots" :
                zz=complex(1,0)
                phase=0
                for zero in self.Czeros:
                    zz*=(p-zero)
                    phase+=np.arctan2((p-zero).imag,(p-zero).real)
                for pole in self.Cpoles:
                    zz/=(p-pole)
                    phase-=np.arctan2((p-pole).imag,(p-pole).real)
                zz*=gain
                return zz,abs(zz),phase
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
    def __repr__(self):
        if self.type == "roots":
            return f'Ftranfert(zeros={self.zeros},poles={self.poles},gain={self.gain},name="{self.name}")'
        if self.type == "function":
            return f'Ftranfert(num={type(self.num)},den={type(self.den)},gain={self.gain},name="{self.name}")'
    # ------------------------------------------------------------------------------
    def __str__(self):
        """
                          (p-z1)(p-z2)(p-z3)...
            F(p) = gain  ------------------------
                          (p-p1)(p-p2)(p-p3)...
        """
        if self.type == "function": return "FT defined with lambda functions"
        outz=strroot(self.Czeros)
        outp=strroot(self.Cpoles)
        outname=self.name+'(p) = '
        if len(outz) == 0 :
            outz=str(self.gain)
            outgain=''
        else:
            outgain= str(self.gain)+' ' if self.gain !=1 else ''

        lz,lp=len(outz),len(outp)
        diff=(lz-lp)//2
        if diff>0:
            dz,dp=0,diff
        else:
            dz,dp=-diff,0
        spacenum=len(outname)+len(outgain)+dz
        spaceden=len(outname)+len(outgain)+dp
        dashed=max(len(outz),len(outp))
        out='\n'
        if len(outp) !=0 :
            out+=spacenum*' '+outz+'\n'
            out+=outname+outgain+dashed*'-'+'\n'
        else:
            out+=outname+outgain+outz
        out+=spaceden*' '+outp+'\n'
        return out

