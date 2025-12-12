import numpy as np
# class de format d'un float
class nf(float):
    def __repr__(self):
        s = f'{self:.1f}'
        return f'{self:.0f}' if s[-1] == '0' else s
# -----------------------------------------------------------------------------
# différentes fonctions de conversion
# -----------------------------------------------------------------------------
def rad2deg(rad) : return rad*180/np.pi   # radian  -> degrée  (phase)
def deg2rad(deg) : return deg*np.pi/180   # degrée  -> radian  (phase)
def nat2dB(g)    : return 20*np.log10(g)  # naturel -> dB      (gain)
def dB2nat(dB)   : return 10**(dB/20)     # dB      -> naturel (gain)
# -----------------------------------------------------------------------------
# relation de Black de la boucle de contre-réaction unitaire négative (negativ feedback)
# -----------------------------------------------------------------------------
def bo2bf(z)     : return z/(1+z)         # BO      -> BF

# retourne la liste des tuples des valeurs et de leurs occurences d'une liste en entrée 
def multiplicity(L):
    multi=[]
    for l in sorted(list(set(L))):
        count=0
        for e in L :
            if e == l :
                count+=1
        multi.append((l,count))
    return multi

def eval_poly(P,x):
    ev=complex(0.0)
    for k,c in enumerate(P):
        expo=len(self.num)-k-1
        ev+=c*x**expo
    return ev
