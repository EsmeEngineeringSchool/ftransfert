from common.Ftransfert import Ftransfert
from bode.plot import bode as bodeplot 

if __name__ == "__main__" :
    if False:
        gain=1
        num=lambda p : 1
        den=lambda p : 1+p
        H0=Ftransfert(num=num,den=den,gain=gain,name="H_0")
        print(repr(H0))
        print(str(H0))
        print(H0.eval(1,1))
        bode(H0,y1lim=(-35,10),y2lim=(-90,0),n=1024,color="tab:green")
    if True :
        gain=100
        poles=[(-0.01,0),(-0.1,0),(-100,0)]
        zeros=[(-1,0),(-1,0)]
        H2=Ftransfert(zeros=zeros,poles=poles,gain=gain,name="H_2")
        print(repr(H2))
        #bodeplot(H2,fmax=1e5,xlim=(1e-4,1e5),y1lim=(-80,80),y2lim=(-180,0),n=1024,color="tab:green")
        bodetikz(H2)
