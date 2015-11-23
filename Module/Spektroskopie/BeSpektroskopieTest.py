# coding=utf-8
"""
@author: Valon Lushta
@author: Sebastian Badur
"""

import numpy as np
import sys
import os
# from lmfit.models import  #### alternatives Fitten siehe https://lmfit.github.io/lmfit-py/
from lmfit import *
import matplotlib.pyplot as plt
from glob import glob
from nptdms import TdmsFile
from scipy.signal import savgol_filter
from Module.Sonstige import Fehler

"""
#folder = "/home/sebadur/Dokumente/BE-Spektroskopie/2015-11-10 Vergleich/"
folder = "/home/sebadur/Dokumente/BE-Spektroskopie/2015-11-17/Messung 1/"

omega = '1'

fmin = 60000
fmax = 90000
df = 100
messpunkte = (fmax-fmin)//df

mittelungen = 200

bereich_min = 0
bereich_max = messpunkte

amp_min = 0.00001
amp_max = 0.1
guete = 20
guete_min = 5
guete_max = 25
off_min = 0
off_max = 0.005
"""
















def read_tdmsfile(datei, par): # Dateiname aufgeteilt und Nummerisch sortiert
    tdms_file = TdmsFile(datei)
    channel = tdms_file.object('Unbenannt', 'Untitled')     # erster Name ist der Gruppenname dann der Kanalname
    multy = np.array(channel.data)
    datay = np.zeros(par.messpunkte)

    for n in range(par.mittelungen):
        for m in range(par.messpunkte):
            try:
                datay[m] += multy[m+n*par.messpunkte]
            except IndexError:
                break

    anz = len(datay)
    if anz + par.bereich_rechts <= par.bereich_links or par.bereich_links < 0:
        raise Fehler(IndexError())
    elif par.bereich_rechts == 0:
        par.bereich_rechts = anz

    datay = datay[par.bereich_links:par.bereich_rechts]
    datax = range(par.fmin, par.fmax, par.df)[par.bereich_links:par.bereich_rechts]

    return datax, datay




def resonance_lorentz(freq, resfreq, amp, guete, off):
    return amp * resfreq**2 / (
        guete * np.sqrt((freq**2 - resfreq**2)**2 + (freq * resfreq / guete)**2)
    ) + off

mod = Model(resonance_lorentz)




def test_fit(ordner, par):
    debug = 0

    erg_amp = []
    erg_freq = []
    erg_phase = []
    erg_offsets = []


    fnames = glob(ordner+"/amp"+str(par.omega)+"*.tdms")    # alle dateien in diesem Ordner mit der Endung txt

    parameter = []
    for name in fnames:
        pname = name.split(os.sep)[-1].split('amp')[1].split('G')[0]
        try:
            parameter.index(pname)
        except ValueError:
            parameter.append(pname)
    print(parameter)

    for parName in parameter:
        amps = []
        freqs = []
        phase = []
        offsets = []
        fnames = glob(ordner+"/amp"+parName+"*.tdms")
        """fnames = sorted(
            glob(folder+"amp"+par+"*.tdms"),
            key=lambda n: float(n.split('G')[-1].split('V')[0].replace(',', '.'))
        )"""

        for name in fnames:
            out, ph, datx, daty = fit_datei(name, par)

            amps.append(out.best_values["amp"])
            freqs.append(out.best_values["resfreq"])
            phase.append(ph)
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



def fit_datei(name, par):
    datx, daty = read_tdmsfile(name, par)
    phasx, phasy = read_tdmsfile(name.replace('amp', 'phase'), par)  # DAS KANN SO NICHT BLEIBEN (ersetzt nicht nur im Dateinamen, sondern auch im Pfad)

    index_max = np.argmax(daty)
    start_freq = datx[index_max]
    start_amp = daty[index_max]
    start_off = daty[0]

    params = Parameters()
    params.add('resfreq', value=start_freq, min=par.fmin, max=par.fmax)
    params.add('amp', value=start_amp, min=par.amp_min, max=par.amp_max)
    params.add('guete', value=par.guete, min=par.guete_min, max=par.guete_max)
    params.add('off', value=start_off, min=par.off_min, max=par.off_max)

    out = mod.fit(savgol_filter(daty, 51, 5), freq=datx, params=params)

    neben_resfreq = max(min(int((out.best_values["resfreq"] - par.fmin) // par.df + par.messpunkte // 10), len(phasy)-1), 0)
    phase = savgol_filter(phasy, 51, 5)[neben_resfreq] / par.messpunkte

    return out, phase, datx, daty
