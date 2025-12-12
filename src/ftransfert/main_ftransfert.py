from common.Ftransfert import Ftransfert

if __name__ == "__main__" :
    if False :
        #H_0
        gain=1
        num=lambda p : 1
        den=lambda p : 1+p+p**2
        H0=Ftransfert(num=num,den=den,gain=gain,name="H_0")
        print(H0)
        print(repr(H0))
        print(str(H0.latex()))
        print(H0.eval(1,1))
    if False:
        # H_1
        gain=4
        poles=[]
        zeros=[(-1,0),(-2,0)]
        H1=Ftransfert(zeros=zeros,poles=poles,gain=gain,name="H_1")
        print(H1)
        print(H1.latex())
        print(repr(H1))
        H1.info()

    if False:
        # H_2
        gain=1
        zeros=[(1,-1),(1,1),(-3,7)]
        poles=[(-1,0),(-2,0)]
        H2=Ftransfert(zeros=zeros,poles=poles,gain=gain,name="H_2")
        print(H2)
        print(repr(H2))

        #FT roots
        zeros=[(-1,0),(-4,0),(-3,0)]
        poles=[(-0.75,-0.25),(-0.75,0.5)]
        gain=0.25
        F=Ftransfert(zeros=zeros,poles=poles,gain=gain,name="F")
        print(F)
        print(F.latex())
        print(repr(F))

    if True :
        gain=100
        poles=[(-0.01,0),(-0.1,0),(-100,0)]
        zeros=[(-1,0),(-1,0)]
        H2=Ftransfert(zeros=zeros,poles=poles,gain=gain,name="H_2")
        print(f"str : {H2}")
        print(f"H2(1j) = {H2.eval(1j)}")
        H2.info()
        num=lambda p:(p+1)**2
        den=lambda p: (p+100)*(p+0.1)*(p+0.01)
        H2=Ftransfert(num=num,den=den,gain=gain,name="H_2")
        print(f"str : {H2}")
        print(f"H2(1j) = {H2.eval(1j)}")
        H2.info()
        num=[1,2,1]  #p**2+2p+1 
        den=[1,100.11,11.001,0.1]  #p**3+100.11*p**2+11.001*p+0.1
        H2=Ftransfert(num=num,den=den,gain=gain,name="H_2")
        print(f"str : {H2}")
        print(f"H2(1j) = {H2.eval(1j)}")
        H2.info()
