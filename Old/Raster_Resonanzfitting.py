# -*- coding: utf-8 -*-
"""
Created on 11.11.14

@author: valon lushta

Skript zum Fitten von Resonanzkurven in einem Raster.


"""
import numpy as np
import scipy
from scipy.optimize import leastsq
from scipy.signal import savgol_filter # (x, window_length, polyorder, deriv=0, delta=1.0, axis=-1, mode='interp', cval=0.0)
import matplotlib.pyplot as plt
from nptdms import TdmsFile
from netCDF4 import Dataset
from glob import glob
import sys
import time
from scipy import signal# signal.savgol_filter(x,window,order)

start_time = time.time()

######## Definitionen '''''''''''''''''''''''###
def resonance_lorentz(p,x):   #x ist freq, p[1] drive amplitude, p[o] resonanzfreq, p[2] ist die Guete
    return p[1]*(np.power(p[0],2)/p[2])/(np.sqrt((np.power(np.power(x,2)-np.power(p[0],2),2)+np.power((x*p[0]/p[2]),2))))    #lorentz funktion

def resonance_lorentz_errorfunc(p,x,z):
        return resonance_lorentz(p,x)-z

def drive_lorentz(p,x):   #x ist freq, p[1] drive amplitude, p[o] resonanzfreq, p[2] ist die Guete
    return p[1]*np.power(p[0],2)/(np.sqrt((np.power(np.power(x,2)-np.power(p[0],2),2)+np.power((x*p[0]/p[2]),2))))    #lorentz funktion

def drive_lorentz_errorfunc(p,x,z):
        return drive_lorentz(p,x)-z

def phase_lorentz(p,x):
    return np.arctan((x*p[0]/p[2])/(np.power(x,2)-np.power(p[0],2)))

def phase_errorfunc(p,x,z):
        return phase_lorentz(p,x)-z

def func_fit_leastsquare(x,y,errorfunc,p0,freq,amp_list):
    solp, convx, infodict, mesg, ier = leastsq(errorfunc, 
                            p0, 
                            args=(freq,amp_list),
                            Dfun=None,
                            full_output=True,
                            ftol=1e-9,
                            xtol=1e-9,
                            maxfev=50000,
                            epsfcn=1e-10,
                            factor=0.1)
    fitparameter=np.array(solp, dtype=float)
    return fitparameter,solp,convx,infodict,mesg,ier

def split_list(alist, wanted_parts=1):
    length = len(alist)
    return [ alist[i*length // wanted_parts: (i+1)*length // wanted_parts] 
             for i in range(wanted_parts) ]

#### Plot definitions ###
def standard_plot(name,x,y1,ylabl,leg_loc=1):
    fig = plt.figure(name)
    ax = fig.add_subplot(111)
    ax.plot(x,y1, '-', label = '')
    #ax.legend(loc=leg_loc)
    ax.grid()
    ax.set_xlabel("Pixel (#)")
    ax.set_ylabel(ylabl)
    #ax.set_ylim(-20,100)
    #ax.set_ylim(-180,180)
    plt.show()

def save_ncfile(name,pixel,data_out):
    ncfile=Dataset(name+'.nc','w')
    ncfile.createDimension('x',pixel)
    ncfile.createDimension('y',pixel)
    dd=ncfile.createVariable(name,np.dtype('int32').char,('x','y'))
    data_out2=np.int32(((data_out+abs(data_out.min()))/(data_out.max()-data_out.min()))*(np.power(2,31)-1))
    dd[:] = data_out2
    ncfile.close()

data=[]
phase=[]
messpunkte=200 # die Anzahl der Messpunkte pro Resonanzkurve
pixel=200	# anzahl der Resonanzkurven

############## TDMS Datei einlesen ''''''''''''''''''''''''''''''''''''''
fnames=glob("/home/sebadur/Dokumente/Studium/Master/Fit-GUI/Messung 06.11.14/amp*.tdms")    # alle dateien in diesem Ordner mit der Endung TDMS
sorted_fnames = sorted(fnames, key=lambda x: int(x.split('/')[-1].split('amp')[1].split('.')[0]))    # Dateiname aufgeteilt und Nummerisch sortiert
for i in range(pixel):
    tdms_file = TdmsFile(sorted_fnames[i])
    channel = tdms_file.object('Unbenannt', 'Untitled')     # erster Name ist der Gruppenname dann der Kanalname
    data.append(np.array(channel.data))

###################--phase-- ############################
fnames=glob("/home/sebadur/Dokumente/Studium/Master/Fit-GUI/Messung 06.11.14/phase*.tdms")    # alle dateien in diesem Ordner mit der Endung TDMS
sorted_fnames = sorted(fnames, key=lambda x: int(x.split('/')[-1].split('phase')[1].split('.')[0]))    # Dateiname aufgeteilt und Nummerisch sortiert
for i in np.arange(pixel):
    tdms_file = TdmsFile(sorted_fnames[i])
    channel = tdms_file.object('Unbenannt', 'Untitled')     # erster Name ist der Gruppenname dann der Kanalname
    #data[i]=np.array(channel.data)
    phase.append(np.array(channel.data))



if pixel!=len(data[1])/messpunkte:
  print('Check Pixel Setting')

freqmin=203000 # minimal Frequenz
freqmax=223000 # maximal Frequenz
dfreq=float((freqmax-freqmin)/float(messpunkte))
freq=np.arange(freqmin,freqmax,dfreq)# definition der Frequenz

p0 = np.array([(freqmax-freqmin)/2+freqmin, 0.1, 5], dtype=np.double) #Initial guess

fitparameter=np.zeros((pixel,pixel,3))
error_fitparameter=np.zeros((pixel,pixel,3))
sphase=np.zeros((pixel,pixel,1))   # single phase point off resonance
fitparam1=[]
fit1_Q=[]
fit1_resfreq=[]
fit1_damp=[]
perr1=[]
err1_Q=[]
err1_resfreq=[]
err1_damp=[]
iter_limit=[]
max_iter=[0,0,0,0,0]# [0]-value,[1]-t.[2]-i,[3]-amp_list[i],[4]-solp


for t in range(pixel):		#	y-Axis
    amp=np.array(np.multiply(data[t],100), dtype=np.double)
    amp_list=split_list(amp, wanted_parts=pixel)
    phase1=np.array(phase[t],dtype=np.double)
    phase_list=split_list(phase1,wanted_parts=pixel)
    
    for i in range(pixel):	#	x-Axis
        z=resonance_lorentz(amp_list[i],freq)
        fitparameter[t,i],solp, convx, infodict, mesg, ier = func_fit_leastsquare(i,t,resonance_lorentz_errorfunc,p0,freq,signal.savgol_filter(amp_list[i],15,3)) # fit process starten
        
        ### Berechnung von Standardabweichung
        s_sq = (resonance_lorentz_errorfunc(fitparameter[t,i], freq, amp_list[i])**2).sum()/(len(amp)-len(p0))
        pconx = convx * s_sq
        error = [] 
        for j in range(len(fitparameter[t,i])):
            try:
                error.append( np.absolute(pconx[j][j])**0.5)
            except:
                error.append( 0.00 )
        error_fitparameter[t,i]=error       
        ###############
        
        iterationen=infodict.get('nfev')        
        iter_limit.append(iterationen)        
        """if iterationen > 100:
            iter_limit.append(0)
        else: iter_limit.append(1)
        """
        if max_iter[0]<iterationen:
            max_iter[0]=iterationen
            max_iter[1]=t
            max_iter[2]=i
            max_iter[3]=amp_list[i]
            max_iter[4]=solp
        
        ######### +++ phase-calculation ++++ #####
        smoothed_phase=signal.savgol_filter(phase_list[i],15,3)     
        amp_max=signal.savgol_filter(amp_list[i],15,3)
        ind=np.argmax(amp_max)+20
        sphase[t,i,0]=smoothed_phase[ind]
        
    print(t),
    
    
fit_resfreq=fitparameter[:,:,0]
fit_damp=fitparameter[:,:,1]
fit_Q=fitparameter[:,:,2]
fit_phase=sphase[:,:,0]

err_resfreq=error_fitparameter[:,:,0]
err_damp=error_fitparameter[:,:,1]
err_Q=error_fitparameter[:,:,2]   


# Fehler angaben in Prozent ausgeben
fehler_prozent_resfreq=err_resfreq*100/fit_resfreq
fehler_prozent_damp=err_damp*100/fit_damp
fehler_prozent_Q=err_Q*100/fit_Q



print("\r")
resfreq=np.array(fit_resfreq)#.reshape(pixel,pixel)
resfreq_fehler=np.array(err_resfreq).reshape(pixel,pixel)
print("resfreq calculated")
damp=np.array(fit_damp)#.reshape(pixel,pixel)
damp_fehler=np.array(err_damp).reshape(pixel,pixel)
print("damp calculated")
Q=np.array(fit_Q)#.reshape(pixel,pixel)
Q_fehler=np.array(err_Q).reshape(pixel,pixel)
print("Q-factor calculated")
fphase=np.array(fit_phase).reshape(pixel,pixel)



print('Durchschnittliche Anzahl von Iterationen: %s' %(int(np.average(iter_limit))))
print('Laufzeit: %s seconds ' % str(time.time() - start_time))#### kann auch durch time python rcX.py im terminal gemacht werden

"""###################################################
#Abspeichern als png für gwyddion
img_damp = scipy.misc.toimage(damp, mode='I')#, high=np.max(damp), low=np.min(damp)
img_damp.save('damp.png')

img_damp_fehler = scipy.misc.toimage(damp_fehler, high=np.max(damp_fehler), low=np.min(damp_fehler), mode='I')
img_damp_fehler.save('damp_fehler.png')

img_Q = scipy.misc.toimage(Q, high=np.max(Q), low=np.min(Q), mode='I')
img_Q.save('Q.png')

img_Q_fehler = scipy.misc.toimage(Q_fehler, high=np.max(Q_fehler), low=np.min(Q_fehler), mode='I')
img_Q_fehler.save('Q_fehler.png')

img_resfreq = scipy.misc.toimage(resfreq, high=np.max(resfreq), low=np.min(resfreq), mode='I')
img_resfreq.save('resfreq.png')

img_resfreq_fehler = scipy.misc.toimage(resfreq_fehler, high=np.max(resfreq_fehler), low=np.min(resfreq_fehler), mode='I')
img_resfreq_fehler.save('resfreq_fehler.png')
####################################################
"""
"""
plt.imshow(damp,vmin=0.000,vmax=0.1)
plt.title("Resonanz Amplitude")
plt.colorbar(label='(a.u.)')
plt.show()

plt.imshow(Q,vmin=0,vmax=300)
plt.title("Q-Faktor")
plt.colorbar()
plt.show()

plt.imshow(resfreq,vmin=freqmin+2000,vmax=freqmax-2000)
plt.title("Resonanz Frequenz")
plt.colorbar(label='(Hz)')
plt.show()

plt.imshow(fphase,vmin=-180,vmax=180)
plt.title("Phase")
plt.colorbar(label=r'($^\circ$)')
plt.show()



itt=np.array(iter_limit).reshape(pixel,pixel)
plt.imshow(itt)
plt.title("Iterationen (Drive)")
plt.colorbar()


plt.figure(pixel)
plt.subplot(131)
plt.imshow(fehler_prozent_damp,vmin=fehler_prozent_damp.min(),vmax=sorted(fehler_prozent_damp.max(0))[-3])
plt.title("Fehler Amplitude in Prozent (Drive)")
plt.colorbar()
plt.subplot(132)
plt.imshow(fehler_prozent_resfreq,vmin=fehler_prozent_resfreq.min(),vmax=sorted(fehler_prozent_resfreq.max(0))[-3])
plt.title("Fehler Resonanzfrequenz in Prozent (Drive)")
plt.colorbar()
plt.subplot(133)
plt.imshow(fehler_prozent_Q,vmin=fehler_prozent_Q.min(),vmax=sorted(fehler_prozent_Q.max(0))[-3])
plt.title("Fehler Q-Faktor in Prozent (Drive)")
plt.colorbar()
"""

plt.figure('phase')
plt.imshow(fphase,vmin=-180,vmax=180)
plt.title("Phase")
plt.colorbar(label=r'($^\circ$)')

standard_plot('phasecut',range(pixel),signal.savgol_filter(sphase[99,:,0],11,3),r"Phase ($^\circ$)")

standard_plot('ampcut',range(pixel),signal.savgol_filter(fitparameter[99,:,1],11,3),r"Amplitude (a.u.)")

plt.figure(pixel+1)
plt.subplot(121)
plt.imshow(damp,vmin=fit_damp.min(),vmax=fit_damp.max())
plt.title("Amplitude")
plt.colorbar()

#plt.figure(pixel+11)
plt.subplot(122)
plt.imshow(damp_fehler)#,vmin=min(fit_damp),vmax=max(fit_damp))
plt.title("damp_fehler")
plt.colorbar()


plt.figure(pixel+2)
plt.subplot(121)
plt.imshow(Q,vmin=fit_Q.min(),vmax=fit_Q.max())
plt.title("Q")
plt.colorbar()
#plt.figure(pixel+12)
plt.subplot(122)
plt.imshow(Q_fehler)#,vmin=min(fit_Q),vmax=max(fit_Q))
plt.title("Q_fehler")
plt.colorbar()


plt.figure(pixel+3)
plt.subplot(121)
plt.imshow(resfreq,vmin=freqmin,vmax=freqmax)#sorted(fit_resfreq)[-2])#max(fit_resfreq))
plt.title("resfreq")
plt.colorbar()

#plt.figure(pixel+13)
plt.subplot(122)
plt.imshow(resfreq_fehler)#,vmin=min(fit_resfreq),vmax=max(fit_resfreq))
plt.title("resfreq_fehler")
plt.colorbar()

"""

plt.figure(pixel+4)
plt.scatter(freq, amp_list[163], c='r', marker='+', color='r', label='Measured Data')
plt.plot(freq, resonance_lorentz(fitparameter[199,163],freq), 'g--', linewidth=2, label='leastsq fit')
#plt.xlim((1100, 1300))
#plt.ylim((-0.01, 5))
plt.grid(which='major')
plt.legend(loc=1)
plt.show()

####### Fit mit maximalen itterationen
plt.figure(pixel+5)
plt.scatter(freq, max_iter[3], c='r', marker='+', color='r', label='Measured Data')
plt.plot(freq, resonance_lorentz(max_iter[4],freq), 'g--', linewidth=2, label='leastsq fit')
#plt.xlim((1100, 1300))
#plt.ylim((-0.01, 5))
plt.grid(which='major')
plt.title("Fit maximale Iterationen (Drive)")
plt.legend(loc=1)
plt.show()"""