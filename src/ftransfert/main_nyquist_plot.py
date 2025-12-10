from common.Ftransfert import Ftransfert
from nyquist.plot import nyquist 

if __name__ == "__main__" :
    gain=1
    num=lambda p : 1
    den=lambda p : 1+p+p**2
    H0=Ftransfert(num=num,den=den,gain=gain,name="H_0")
    print(repr(H0))
    print(str(H0))
    print(H0.eval(1,1))
    nyquist(H0,complet=True,mcircles=False,ncircles=False,xlim=(-1,1.5),ylim=(-1.5,1.5),n=1024,color="tab:green")
