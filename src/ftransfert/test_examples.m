%num=[1,2,1]
%den=[1,100.11,11.001,0.1]
num=[1,0,0];  %p**2+2p+1
den=[100,5,1.0];  %p**3+100.11*p**2+11.001*p+0.1
num=[1,1]
den=[0.1,1,0,0]
H=4*4*tf(num,den)
%H=1000*tf(poly(zeros),poly(poles))
bode(H);
dcgain(H)