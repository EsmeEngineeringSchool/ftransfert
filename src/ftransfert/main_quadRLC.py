import subprocess 
import numpy as np
import math
from common.Ftransfert import Ftransfert
from ftransfert.common.utils      import nat2dB, rad2deg
from fromquad.quadRLC import Quad 
from bode.plot import bode as bodeplot
from bode.tikz import bode as bodetikz

def estimation_bounds(R,L,C,H):
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
    return xlim,(g0f,g1f),(-90,90) 

if __name__ == "__main__" :
    R,C,L=1000,1e-6,0.001
    nquad,composants=2,"RLC" 
    #quad=Quad(nquad,composants,series=["R","R"],shunts=["L","R"])
    quad=Quad(nquad,composants)
    quad.random()
    print(quad)
    H=quad.get_ftransfert_from_RLC(R,C,L)
    print(H)
    xlim,y1lim,y2lim=estimation_bounds(R,L,C,H)
    bodeplot(H,xlim=xlim,y1lim=y1lim,y2lim=y2lim,n=1024)
    filename="example_quadRLC.tex"
    bodetikz(H,filename=filename,xlim=xlim,y1lim=y1lim,y2lim=y2lim)
    result = subprocess.run( ["pdflatex", filename], capture_output=True)
    if result.returncode : print("erreur de compilation pdflatex")
