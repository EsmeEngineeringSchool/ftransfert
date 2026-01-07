from ftransfert.common.Ftransfert import Ftransfert
from ftransfert.bode.tikz import bode as bodetikz
from ftransfert.bode.plot import bode as bodeplot

if __name__ == "__main__" :
    if False :
        gain=16
        num=[1,1]
        den=[0.1,1,0,0]
        H=Ftransfert(num=num,den=den,gain=gain,name="H")
        H.info()
        filename="exercice1_1.tex"
        bodetikz(H,filename,xlim=(1e-1,1e2),y1lim=(-40,40),y2lim=(-180,-90))
        bodeplot(H,fmax=1e6,xlim=(1e-1,1e2),y1lim=(-40,40),y2lim=(-180,-90))
    if True :
        gain=40
        zeros=[(-1,0)]
        poles=[(0,0),(0,0),(-10,0)]
        H=Ftransfert(zeros=zeros,poles=poles,gain=gain,name="H")
        H.info()
        print(f"str : {H}")
        print(f"eval jw : {H.eval(1j)}")
        filename="exercice1_1.tex"
        bodetikz(H,filename,xlim=(1e-1,1e2),y1lim=(-40,40),y2lim=(-180,-90))
        bodeplot(H,fmax=1e6,xlim=(1e-1,1e2),y1lim=(-40,40),y2lim=(-180,-90))
    if False :
        gain=1
        num=[4,4]
        #p²(1+0.2p)(1+0.1p) = p²(1+0.3p+0.02p²) = p²+0.3p^3+0.02p^4
        den=[0.02,0.3,1,0,0]
        H=Ftransfert(num=num,den=den,gain=gain,name="H")
        H.info()
        print(f"str : {H}")
        filename="exercice1_2.tex"
        print(f"writing {filename}")
        with open(filename,"w") as f:
            print(bodetikz(H,wlim=(1e-4,1e4),gain_axis=(-80,40,10),phase_axis=(-360,0,20)),file=f)
        bodeplot(H,fmax=1e6,xlim=(1e-4,1e4),y1lim=(-80,40),y2lim=(-360,0))
