from common.Ftransfert import Ftransfert
from bode.tikz import bode as bodetikz

if __name__ == "__main__" :
    if True :
        gain=100
        poles=[(-0.01,0),(-0.1,0),(-100,0)]
        zeros=[(-1,0),(-1,0)]
        H2=Ftransfert(zeros=zeros,poles=poles,gain=gain,name="H_2")
        H2.info()
        print(f"str : {H2}")
        with open("tmp1.tex","w") as f:
            print(bodetikz(H2,wlim=(1e-4,1e4)),file=f)
        num=[1,2,1]  #p**2+2p+1 
        den=[1,100.11,11.001,0.1]  #p**3+100.11*p**2+11.001*p+0.1
        H2=Ftransfert(num=num,den=den,gain=gain,name="H_2")
        print(f"str : {H2}")
        H2.info()
        with open("tmp2.tex","w") as f:
            print(bodetikz(H2,wlim=(1e-4,1e4)),file=f)
