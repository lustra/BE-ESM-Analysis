# coding=utf-8
import numpy as np
import sys
import os
# from lmfit.models import  #### alternatives Fitten siehe https://lmfit.github.io/lmfit-py/
from lmfit import *
import matplotlib.pyplot as plt
from glob import glob
from nptdms import TdmsFile
from scipy.signal import savgol_filter










#folder = "/home/sebadur/Dokumente/BE-Spektroskopie/2015-11-10 Vergleich/"
folder = "/home/sebadur/Dokumente/BE-Spektroskopie/2015-11-16/Messung/"

omega = '1'

fmin = 62000
fmax = 83000
df = 50
messpunkte = (fmax-fmin)//df

mittelungen = 200

bereich_min = 50
bereich_max = messpunkte-50

amp_min = 0.00001
amp_max = 0.1
guete = 20
guete_min = 5
guete_max = 25
off_min = 0
off_max = 0.005


















def read_tdmsfile(folder): # Dateiname aufgeteilt und Nummerisch sortiert
    tdms_file = TdmsFile(folder)
    channel = tdms_file.object('Unbenannt', 'Untitled')     # erster Name ist der Gruppenname dann der Kanalname
    multy = np.array(channel.data)
    datay = np.zeros(messpunkte)

    for n in range(mittelungen):
        for m in range(messpunkte):
            try:
                datay[m] += multy[m+n*messpunkte]
            except IndexError:
                break

    datay = datay[bereich_min:bereich_max]
    datax = range(fmin, fmax, df)[bereich_min:bereich_max]

    return datax, datay




def resonance_lorentz(freq, resfreq, amp, guete, off):
    return amp * resfreq**2 / (
        guete * np.sqrt((freq**2 - resfreq**2)**2 + (freq * resfreq / guete)**2)
    ) + off

mod = Model(resonance_lorentz)





duplicate = []
erg_amp = []
erg_freq = []
erg_phase = []
erg_offsets = []


fnames = glob(folder+"amp"+omega+"*.tdms")    # alle dateien in diesem Ordner mit der Endung txt

parameter = []
for name in fnames:
    pname = name.split(os.sep)[-1].split('amp')[1].split('G')[0]
    try:
        parameter.index(pname)
    except ValueError:
        parameter.append(pname)
print(parameter)

for par in parameter:
    amps = []
    freqs = []
    phase = []
    offsets = []
    fnames = glob(folder+"amp"+par+"*.tdms")
    """fnames = sorted(
        glob(folder+"amp"+par+"*.tdms"),
        key=lambda n: float(n.split('G')[-1].split('V')[0].replace(',', '.'))
    )"""
    for name in fnames:
        datx, daty = read_tdmsfile(name)
        phasx, phasy = read_tdmsfile(name.replace('amp', 'phase'))  # DAS KANN SO NICHT BLEIBEN (ersetzt nicht nur im Dateinamen, sondern auch im Pfad)

        index_max = np.argmax(daty)
        start_freq = datx[index_max]
        start_amp = daty[index_max]
        start_off = daty[0]

        params = Parameters()
        params.add('resfreq', value=start_freq, min=fmin, max=fmax)
        params.add('amp', value=start_amp, min=amp_min, max=amp_max)
        params.add('guete', value=guete, min=guete_min, max=guete_max)
        params.add('off', value=start_off, min=off_min, max=off_max)

        out = mod.fit(savgol_filter(daty, 51, 5), freq=datx, params=params)
        #mod = Minimizer(resonance_lorentz, params)
        #out = mod.leastsq(params, maxfev=sys.maxint)

        if name in [
            "/home/sebadur/Dokumente/BE-Spektroskopie/2015-11-16/Messung/amp1w10,000000G-5,000000V.tdms",
            "/home/sebadur/Dokumente/BE-Spektroskopie/2015-11-16/Messung/amp1w10,000000G-4,000000V.tdms",
            "/home/sebadur/Dokumente/BE-Spektroskopie/2015-11-16/Messung/amp1w10,000000G-3,000000V.tdms"
        ]:
            print(name)
            print("amp="+str(out.best_values["amp"])+", resfreq="+str(out.best_values["resfreq"])+", güte="+str(out.best_values["guete"])+", off="+str(out.best_values["off"]))
            plt.plot(datx, daty)
            plt.plot(datx, out.best_fit, 'r')
            plt.show()

            plt.plot(phasx, savgol_filter(phasy//messpunkte, 51, 5))
            plt.plot([phasx[messpunkte//4], phasx[messpunkte//4]], [phasy.max()//messpunkte, phasy.min()//messpunkte], 'r')
            plt.show()

        amps.append(out.best_values["amp"])
        freqs.append(out.best_values["resfreq"])
        phase.append(savgol_filter(phasy, 51, 5)[messpunkte//4]/messpunkte)
        offsets.append(float(name.split('G')[-1].split('V')[0].replace(',', '.')))

    erg_amp.append(np.array(amps))
    erg_freq.append(np.array(freqs))
    erg_phase.append(np.array(phase))
    erg_offsets.append(np.array(offsets))



for i in range(len(parameter)):
    plt.plot(erg_offsets[i], erg_amp[i], '.', label=parameter[i])
plt.legend(loc=9)
plt.ylabel('Amplitude (FFT a.u.)')
plt.xlabel('Offset (V)')
plt.show()

for i in range(len(parameter)):
    plt.plot(erg_offsets[i], erg_freq[i], '.', label=parameter[i])
plt.legend(loc=9)
plt.ylabel('Resonanzfrequenz (Hz)')
plt.xlabel('Offset (V)')
plt.show()

for i in range(len(parameter)):
    plt.plot(erg_offsets[i], erg_phase[i], '.', label=parameter[i])
plt.legend(loc=9)
plt.ylabel('Phase (Grad)')
plt.xlabel('Offset (V)')
plt.show()

print 'finished!'

