# coding=utf-8
import numpy as np
import os
from lmfit.models import * #### alternatives Fitten siehe https://lmfit.github.io/lmfit-py/
from lmfit import *
import matplotlib.pyplot as plt
from glob import glob
from nptdms import TdmsFile





def read_tdmsfile(folder): # Dateiname aufgeteilt und Nummerisch sortiert
    tdms_file = TdmsFile(folder)
    channel = tdms_file.object('Unbenannt', 'Untitled')     # erster Name ist der Gruppenname dann der Kanalname
    multy = np.array(channel.data)
    datay = np.zeros(1050)

    for n in range(100):
        for m in range(1050):
            try:
                datay[m] += multy[m+n*1050]
            except IndexError:
                break

    datay = datay[150:900]
    datax = range(62000, 83000, 20)[150:900]

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

#folder = "/home/sebadur/Dokumente/BE-Spektroskopie/2015-11-10 Vergleich/"
folder = "/home/sebadur/Dokumente/BE-Spektroskopie/2015-11-10/"


fnames = glob(folder+"amp2*.tdms")    # alle dateien in diesem Ordner mit der Endung txt

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
    for name in fnames:
        datx, daty = read_tdmsfile(name)
        phasx, phasy = read_tdmsfile(name.replace('amp', 'phase'))  # DAS KANN SO NICHT BLEIBEN (ersetzt nicht nur im Dateinamen, sondern auch im Pfad)

        index_max = np.argmax(daty)
        start_freq = datx[index_max]
        start_amp = daty[index_max]
        start_off = daty[0]

        params = Parameters()
        params.add('resfreq', value=start_freq, min=62000, max=72000)
        params.add('amp', value=start_amp, min=0.00001, max=0.1)
        params.add('guete', value=50)
        params.add('off', value=start_off, min=0.00001, max=0.0005)

        out = mod.fit(daty, freq=datx, params=params, verbose=False)
        # out = mod.fit(daty, freq=datx, resfreq=start_freq, amp=start_amp, guete=10, off=start_off, verbose=False)

        if name in ["/home/sebadur/Dokumente/BE-Spektroskopie/2015-11-10 Vergleich/amp1w8,000000G-2,000000V.tdms",
                    "/home/sebadur/Dokumente/BE-Spektroskopie/2015-11-10 Vergleich/amp1w8,000000G-1,000000V.tdms",
                    "/home/sebadur/Dokumente/BE-Spektroskopie/2015-11-10 Vergleich/amp1w8,000000G0,000000V.tdms",
                    "/home/sebadur/Dokumente/BE-Spektroskopie/2015-11-10 Vergleich/amp1w8,000000G1,000000V.tdms"] and False:
            print(name)
            plt.plot(datx, daty)
            plt.plot(datx, out.best_fit, 'r')
            plt.show()

            plt.plot(phasx, phasy)
            plt.show()

        amps.append(out.best_values["amp"])
        freqs.append(out.best_values["resfreq"])
        phase.append(phasy[index_max])
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

