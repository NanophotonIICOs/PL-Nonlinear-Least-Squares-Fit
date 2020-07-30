"""



This code was development for a Physical Engenering degree tesis,
where we are trying fit by Nonlinear Least Squares the parameters of the
Photoluminiscence Spectra of Coupled Quantum Wells.

In these spectra see two transitions, for this reason we propose a sum of Gaussians
or Lorentzianz. In the written work, we propouse Gaussians, bot we have seaw leter
that Lorentzians are a better bet.


"""


#----------------Libreries
import numpy as np
from scipy.optimize import leastsq
import matplotlib.pyplot as plt

#---------------- Temperature of the spectra [Kelvin]
Temperature=12

#----------------Line Form Propose (In this case, Lorentzian)
def norm(x, mean, sd, I):
  norm = []
  for i in range(x.size):
      norm += [(I)*(sd/((x[i] - mean)**2+sd**2))*1/(1+np.exp((x[i] - mean)/(Temperature*0.000086173324)))]
  return np.array(norm)


#---------------- Experimental File (2D array espectra)
fileExp='Example_Experimental_Data.dat'



#---------------- Import data into array.
dataExp= np.loadtxt(fileExp, dtype=np.str, delimiter='\t')
tamExp=(float(dataExp.size))/2
dataExpX=np.zeros(int(tamExp))
for i in range(0,int(tamExp)):
    dataExpX[i]=dataExp[i,0]
dataExpY=np.zeros(int(tamExp))
for i in range(0,int(tamExp)):
    dataExpY[i]=dataExp[i,1]
x=dataExpX
y_real=dataExpY


#---------------- Guess for the initial parameters
"""
Being an iterative method, we need to initialize the variables in the next order:
    
   [Mean1,DeltaMean=Mean2-Mean1, Halfwidth1, Halfwidth2, Intensity0_1, Intensity0_2]
   
Defining DeltaMean we make sure that the second transition will be diferent from the
first.

While better be the initial guess, faster and correct will be the fit.

"""
m, dm, sd1, sd2, I1, I2 = [1.532, 0.005, 0.0014, 0.0016, 0.00007, 0.0002482]
p = [m, dm, sd1, sd2, I1, I2]
y_init = norm(x, m, sd1,I1) + norm(x, m + dm, sd2, I2)


#---------------- Nonlinear Least Squares
def res(p, y, x):
  m, dm, sd1, sd2, I1, I2 = p
  m1 = m
  m2 = m1 + dm
  y_fit = norm(x, m1, sd1, I1) + norm(x, m2, sd2, I2)
  err = y - y_fit
  return err
plsq = leastsq(res, p, args = (y_real, x))
y_est = norm(x, plsq[0][0], plsq[0][2], plsq[0][4]) + norm(x, plsq[0][0] + plsq[0][1], plsq[0][3], plsq[0][5])



#---------------- Plot
plt.figure(figsize=(7.58,5))
plt.plot(x, y_init, 'r.', label='Initial_Guess')
plt.plot(x, y_est, 'g-',linewidth=3, label='Fitted')
plt.plot(x, y_real, label='Experimental_Data')
plt.legend()
plt.show()



#----------------Printing Parameters

print("-----------Parameters----------")

print("Mean_1: "+str(plsq[0][0]))
print("Mean_2: "+str(plsq[0][0] + plsq[0][1]))
print("\n")

print("Intensity_1: "+str(plsq[0][4]))
print("Intensity_2: "+str(plsq[0][5]))
print("\n")

print("Halfwidth_1: "+str(plsq[0][2]))
print("Halfwidth_2: "+str(plsq[0][3]))
print("\n")


#---------------- Export Fit
Aux=y_est
Nombre='Fit_'+fileExp
f= open(Nombre,"w+")
for i in range(0,int(tamExp)):
    f.write(str(x[i])+"\t")
    f.write(str(Aux[i])+"\n")
f.close() 




#---------------- Export Parameters
Aux=0
Nombre='Params_'+fileExp
f= open(Nombre,"w+")
Aux=plsq[0][0]
f.write("Media1: "+str(Aux)+"\n\n")
Aux=plsq[0][0] + plsq[0][1]
f.write("Media2: "+str(Aux)+"\n\n")
Aux=plsq[0][2]
f.write("Halfwidth1: "+str(Aux)+"\n\n")
Aux=plsq[0][3]
f.write("Halfwidth2: "+str(Aux)+"\n\n")
f.close() 



























