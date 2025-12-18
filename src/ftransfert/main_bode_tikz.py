import numpy as np
from common.Ftransfert import Ftransfert
from bode.tikz import bode as bodetikz

if __name__ == "__main__" :
    if True :
        gain=2
        num=[1,1]
        A=np.polymul([1,10],[1,2])
        A=np.polymul(A,[1,0])
        den=list(map(int,A))
        H=Ftransfert(num=num,den=den,gain=gain,name="H")
        print(H)
        bodetikz(H,filename="example_bodetikz_1.tex",wlim=(1e-2,1e2),gain_axis=(-40,40,10),phase_axis=(-180,0,20),n=1024)

    if True :
        gain=2
        zeros=[(-1,0)]
        poles=[(0,0),(-10,0),(-2,0)]
        H=Ftransfert(zeros=zeros,poles=poles,gain=gain,name="H")
        print(H)
        bodetikz(H,filename="example_bodetikz_2.tex",wlim=(1e-2,1e2),gain_axis=(-40,40,10),phase_axis=(-180,0,20),n=1024)


    if True :
        gain=1000
        zeros=[(-0.001,0),(-1,0)]
        poles=[(-0.01,0),(-0.1,0),(-100,0)]
        H=Ftransfert(zeros=zeros,poles=poles,gain=gain,name="H")
        H.info()
        print(f"str : {H}")
        bodetikz(H,filename="tmp1.tex",wlim=(1e-4,1e4),gain_axis=(-20,40,10),phase_axis=(-90,60,10))

    if True :
        gain=1000
        num=[1,2,1]  #p**2+2p+1 
        den=[1,100.11,11.001,0.1]  #p**3+100.11*p**2+11.001*p+0.1
        H=Ftransfert(num=num,den=den,gain=gain,name="H")
        print(f"str : {H}")
        H.info()
        bodetikz(H,filename="tmp2.tex",wlim=(1e-4,1e4),gain_axis=(-20,40,10),phase_axis=(-90,60,10))

    if True :
        gain=1000
        num=[1,0,0]
        den=[100,5,1]
        H=Ftransfert(num=num,den=den,gain=gain,name="H")
        print(f"str : {H}")
        H.info()
        bodetikz(H,filename="tmp3.tex",wlim=(1e-4,1e4),gain_axis=(-40,80,10),phase_axis=(0,180,20))

    if True :
        gain=1000
        num=[1,0,0]
        den=[1,100.11,11.001,0.1]
        H=Ftransfert(num=num,den=den,gain=gain,name="H")
        print(f"str : {H}")
        H.info()
        bodetikz(H,filename="tmp4.tex",wlim=(1e-4,1e4),gain_axis=(-80,20,20),phase_axis=(-90,180,20))

