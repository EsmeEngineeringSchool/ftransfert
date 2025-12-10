from common.Ftransfert import Ftransfert

if __name__ == "__main__" :
    #H_0
    gain=1
    num=lambda p : 1
    den=lambda p : 1+p+p**2
    H0=Ftransfert(num=num,den=den,gain=gain,name="H_0")
    print(repr(H0))
    print(str(H0))
    print(H0.eval(1,1))
    # H_1
    gain=4
    poles=[]
    zeros=[(-1,0),(-2,0)]
    H1=Ftransfert(zeros=zeros,poles=poles,gain=gain,name="H_1")
    print(repr(H1))
    print(str(H1))

    # H_2
    gain=1
    zeros=[(1,-1),(1,1),(-3,7)]
    poles=[(-1,0),(-2,0)]
    H2=Ftransfert(zeros=zeros,poles=poles,gain=gain,name="H_2")
    print(repr(H2))
    print(str(H2))

    #FT roots
    zeros=[(-1,0),(-4,0),(-3,0)]
    poles=[(-0.75,-0.5),(-0.75,0.5)]
    gain=0.25
    F=Ftransfert(zeros=zeros,poles=poles,gain=gain,name="F")
    print(repr(F))
    print(str(F))
