import numpy as np
import sympy as sp
TWO_PI=2*np.pi    # 2π
HALF_PI=0.5*np.pi # π/2
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

# retourne la liste des tuples des valeurs et de leurs occurences d'une liste de tuplesen entrée 
def multiplicity(L,sign):
    multi=[]
    for l in sorted(list(set(L))):
        count=0
        for e in L :
            if e == l :
                count+=1
        multi.append((l,sign*count))
    return multi

# ------------------------------------------------------------------------------
# évaluation numérique d'un polynome en x.
# P(x) 
def eval_poly(P,x):
    ev=complex(0.0)
    for k,c in enumerate(P):
        expo=len(P)-k-1
        ev+=c*x**expo
    return ev
# ------------------------------------------------------------------------------
# évaluation symbolique d'un polynome par symb
def eval_poly_symbol(P,symb):
    expr=0.0
    for k,c in enumerate(P):
        expo=len(P)-k-1
        expr+=c*symb**expo
    return expr
# ------------------------------------------------------------------------------
def atanN(FT,y,x):
   """
   Généralisation de la fonction atan2(y,x)
   pour compter l'indice de la surface de Riemann.
   note : ça fonctionne mais est-ce que c'est pas un
   overkill de quelque chose de plus simple.
   """
   if x > 0 :
       N=FT.riemann[0]
       return np.arctan(y/x)-N*TWO_PI
   elif x<0 and y>=0 :
       if FT.riemann[1] == -1 :
           FT.riemann[0]+=1
           FT.riemann[1]= 1
       N=FT.riemann[0]
       return np.arctan(y/x)+np.pi-N*TWO_PI
   elif x<0 and y<0 :
       if FT.riemann[1] == 1 :
           FT.riemann[0]-=1
           FT.riemann[1]=-1
       N=FT.riemann[0]
       return np.arctan(y/x)-np.pi-N*TWO_PI
   elif x==0 and y>0 :
       N=FT.riemann[0]
       return HALF_PI-N*TWO_PI
   elif x==0 and y<0 :
       N=FT.riemann[0]
       return -HALF_PI-N*TWO_PI
   elif x==0 and y==0:
       return
# factoriser un polynome par le coefficient non nul 
# de plus petit degré
# exemple :
#   - [1,2,3]   -> [1/3,2/3,1]
#   - [1,2,3,0] -> [1/3,2/3,1,0]      
def factorise(poly):
    for coeff in reversed(poly):
        if coeff == 0.0 : continue
        fact = coeff
        break
    return [coeff/fact for coeff in poly]
# test si une valeur x est dans un iterable à avec certaine tolérance
# absolute(a - b) <= (atol + rtol * absolute(b))
# c.f np.isclose
def isin_tol(x, iterable, rtol=1e-9, atol=0.0):
    return any(np.isclose(x, y, rtol=rtol, atol=atol) for y in iterable)
