
from common.Ftransfert import Ftransfert
from black_nichols.plot import black_nichols

if __name__ == "__main__" :
    gain=1
    num=lambda p : 1
    den=lambda p : 1+p
    H0=Ftransfert(num=num,den=den,gain=gain,name="H_0")
    print(repr(H0))
    print(str(H0))
    print(H0.eval(1,1))
    black_nichols(H0,y1lim=(-35,10),y2lim=(-90,0),n=1024,color="tab:green")
