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
        H=Ftransfert(num=num,den=den,gain=gain,name="H")
        bodeplot(H,xlim=(1e-2,1e2),y1lim=(-40,40),y2lim=(-180,0),n=1024)
        bodetikz(H,filename="example_bodetikz_1.tex",wlim=(1e-2,1e2),gain_axis=(-40,40,10),phase_axis=(-180,0,20),n=1024)

    if True :
        gain=4
        zeros=[(-1,0)]
        poles=[(0,0),(-10,0),(-2,0)]
        H=Ftransfert(zeros=zeros,poles=poles,gain=gain,name="H")
        bodeplot(H,xlim=(1e-2,1e2),y1lim=(-40,40),y2lim=(-180,0),n=1024,color="tab:green")
        bodetikz(H,filename="example_bodetikz_2.tex",wlim=(1e-2,1e2),gain_axis=(-40,40,10),phase_axis=(-180,0,20),n=1024)

