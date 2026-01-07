import matplotlib.pyplot as plt
import subprocess 
import numpy as np
from common.Ftransfert import Ftransfert
from bode.plot import bode as bodeplot
from bode.tikz import bode as bodetikz

if __name__ == "__main__" :

    if True :
        gain=4
        num=[1,1]
        A=np.polymul([1,10],[1,2])
        A=np.polymul(A,[1,0])
        den=list(map(int,A))
        xlim,y1lim,y2lim=(1e-2,1e2),(-80,80),(-180,0)
        H=Ftransfert(num=num,den=den,gain=gain,name="H")
        fig = bodeplot(H,xlim=xlim,y1lim=y1lim,y2lim=y2lim,n=1024)
        plt.show()
        filename="example_bodetikz_1.tex"
        bodetikz(H,filename=filename,xlim=xlim,y1lim=y1lim,y2lim=y2lim)
        result = subprocess.run( ["pdflatex", filename], capture_output=True)
        if result.returncode : print("erreur de compilation pdflatex")


    if True :
        gain=4
        zeros=[(-1,0)]
        poles=[(0,0),(-10,0),(-2,0)]
        H=Ftransfert(zeros=zeros,poles=poles,gain=gain,name="H")
        xlim,y1lim,y2lim=(1e-2,1e2),(-80,80),(-180,0)
        fig = bodeplot(H,xlim=xlim,y1lim=y1lim,y2lim=y2lim,n=1024)
        plt.show()
        filename="example_bodetikz_2.tex"
        bodetikz(H,filename=filename,xlim=xlim,y1lim=y1lim,y2lim=y2lim)
        result = subprocess.run( ["pdflatex", filename], capture_output=True)
        if result.returncode : print("erreur de compilation pdflatex")

