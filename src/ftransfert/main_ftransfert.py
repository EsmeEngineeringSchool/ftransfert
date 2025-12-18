from common.Ftransfert import Ftransfert

if __name__ == "__main__" :
    if False :
        gain=1
        num=lambda p : 1
        den=lambda p : 1+p+p**2
        H=Ftransfert(num=num,den=den,gain=gain,name="H")
        print(H)
        print(repr(H))
        print(str(H.latex()))
        print(H.eval(1,1))
        H.info()

    if True:
        gain=1
        poles=[]
        zeros=[(-1,0),(-2,0)]
        H=Ftransfert(zeros=zeros,poles=poles,gain=gain,name="H")
        print(H)
        print(H.latex())
        print(repr(H))
        H.info()

    if False:
        gain=1
        zeros=[(1,-1),(1,1),(-3,7)]
        poles=[(-1,0),(-2,0)]
        H=Ftransfert(zeros=zeros,poles=poles,gain=gain,name="H")
        print(H)
        print(repr(H))

    if False:
        zeros=[(-1,0),(-4,0),(-3,0)]
        poles=[(-0.75,-0.25),(-0.75,0.5)]
        gain=0.25
        H=Ftransfert(zeros=zeros,poles=poles,gain=gain,name="H")
        print(H)
        print(H.latex())
        print(repr(H))

    if False :
        gain=100
        poles=[(-0.01,0),(-0.1,0),(-100,0)]
        zeros=[(-1,0),(-1,0)]
        H=Ftransfert(zeros=zeros,poles=poles,gain=gain,name="H")
        print(f"str : {H}")
        print(f"H(1j) = {H.eval(1j)}")
        H.info()

    if False :
        num=lambda p:(p+1)**2
        den=lambda p: (p+100)*(p+0.1)*(p+0.01)
        H=Ftransfert(num=num,den=den,gain=gain,name="H")
        print(f"str : {H}")
        print(f"H(1j) = {H.eval(1j)}")
        H.info()

    if False :
        num=[1,2,1]  #p**2+2p+1 
        den=[1,100.11,11.001,0.1]  #p**3+100.11*p**2+11.001*p+0.1
        H=Ftransfert(num=num,den=den,gain=gain,name="H")
        print(f"str : {H}")
        print(f"H(1j) = {H.eval(1j)}")
        H.info()
