from common.Ftransfert import Ftransfert
from bode.tikz import bode as bodetikz

if __name__ == "__main__" :
    if True :
        gain=1000
        zeros=[(-0.001,0),(-1,0)]
        poles=[(-0.01,0),(-0.1,0),(-100,0)]
        H=Ftransfert(zeros=zeros,poles=poles,gain=gain,name="H")
        H.info()
        print(f"str : {H}")
        filename="tmp1.tex"
        print(f"writing {filename}")
        with open(filename,"w") as f:
            print(bodetikz(H,wlim=(1e-4,1e4),gain_axis=(-20,40,10),phase_axis=(-90,60,10)),file=f)
    if True :
        gain=1000
        num=[1,2,1]  #p**2+2p+1 
        den=[1,100.11,11.001,0.1]  #p**3+100.11*p**2+11.001*p+0.1
        H=Ftransfert(num=num,den=den,gain=gain,name="H")
        print(f"str : {H}")
        H.info()
        filename="tmp2.tex"
        print(f"writing {filename}")
        with open(filename,"w") as f:
            print(bodetikz(H,wlim=(1e-4,1e4),gain_axis=(-20,80,20),phase_axis=(-180,0,20)),file=f)

    if True :
        gain=1000
        num=[1,0,0]
        den=[100,5,1]
        H=Ftransfert(num=num,den=den,gain=gain,name="H")
        print(f"str : {H}")
        H.info()
        filename="tmp3.tex"
        print(f"writing {filename}")
        with open(filename,"w") as f:
            print(bodetikz(H,wlim=(1e-4,1e4),gain_axis=(-40,80,10),phase_axis=(0,180,20)),file=f)

    if True :
        gain=1000
        num=[1,0,0]
        den=[1,100.11,11.001,0.1]
        H=Ftransfert(num=num,den=den,gain=gain,name="H")
        print(f"str : {H}")
        H.info()
        filename="tmp4.tex"
        print(f"writing {filename}")
        with open(filename,"w") as f:
            print(bodetikz(H,wlim=(1e-4,1e4),gain_axis=(-80,20,20),phase_axis=(-90,180,20)),file=f)

