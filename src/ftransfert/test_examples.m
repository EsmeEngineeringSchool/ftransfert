%num=[1,0,0];  %p**2+2p+1
%den=[100,5,1.0];  %p**3+100.11*p**2+11.001*p+0.1
zeros=[-0.001,-1]
poles=[-0.01,-0.1,-100]
%H=tf(num,den)
H=1000*tf(poly(zeros),poly(poles))
bode(H);
dcgain(H)