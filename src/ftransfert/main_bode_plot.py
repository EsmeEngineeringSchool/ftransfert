import numpy as np
from common.Ftransfert import Ftransfert
from bode.plot import bode as bodeplot

if __name__ == "__main__" :

    if True :
        gain=5
        num=[1,1]
        A=np.polymul([1,10],[1,2])
        A=np.polymul(A,[1,0])
        den=list(map(int,A))
        H=Ftransfert(num=num,den=den,gain=gain,name="H")
        print(H)
        bodeplot(H,xlim=(1e-2,1e2),y1lim=(-40,40),y2lim=(-180,0),n=1024)

    if True :
        gain=5
        zeros=[(-1,0)]
        poles=[(0,0),(-10,0),(-2,0)]
        H=Ftransfert(zeros=zeros,poles=poles,gain=gain,name="H")
        print(H)
        bodeplot(H,xlim=(1e-2,1e2),y1lim=(-40,40),y2lim=(-180,0),n=1024,color="tab:green")

    if False:
        gain=1
        num=lambda p : 1
        den=lambda p : 1+p
        H=Ftransfert(num=num,den=den,gain=gain,name="H")
        print(H)
        bodeplot(H,y1lim=(-35,10),y2lim=(-90,0),n=1024,color="tab:green")

    if False :
        gain=100
        poles=[(-0.01,0),(-0.1,0),(-100,0)]
        zeros=[(-1,0),(-1,0)]
        H=Ftransfert(zeros=zeros,poles=poles,gain=gain,name="H")
        print(H)
        bodeplot(H,fmax=1e4,xlim=(1e-4,1e4),y1lim=(-80,80),y2lim=(-180,0),n=1024,color="tab:green")

    if False :
        gain=1000
        num=[1,0,0]
        den=[100,5,1]
        H=Ftransfert(num=num,den=den,gain=gain,name="H")
        print(H)
        bodeplot(H,fmax=1e4,xlim=(1e-2,1e0),y1lim=(-20,30),y2lim=(0,180),n=1024,color="tab:green")
