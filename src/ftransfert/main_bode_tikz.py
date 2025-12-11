from common.Ftransfert import Ftransfert
from bode.tikz import bode as bodetikz

if __name__ == "__main__" :
    with open("tmp.tex","w") as f:
        if True :
            gain=100
            poles=[(-0.01,0),(-0.1,0),(-100,0)]
            zeros=[(-1,0),(-1,0)]
            H2=Ftransfert(zeros=zeros,poles=poles,gain=gain,name="H_2")
            print(H2)
            print(bodetikz(H2),file=f)
