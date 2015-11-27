# coding=utf-8
"""
@author: Valon Lushta
@author: Sebastian Badur
"""

import numpy as np
import os
# from lmfit.models import  #### alternatives Fitten siehe https://lmfit.github.io/lmfit-py/
from lmfit import *
import matplotlib.pyplot as plt
from glob import glob
from nptdms import TdmsFile
from scipy.signal import savgol_filter
from Module.Sonstige import Fehler


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
    """
    :type ordner: str
    :type par: Module.Spektroskopie.Parameter.Parameter
    """
    if not ordner.endswith(os.sep):
        ordner += os.sep

    erg_amp = []
    erg_freq = []
    erg_phase = []
    erg_offsets = []

    dateien = glob(ordner + 'amp' + str(par.omega) + '*.tdms')

    """parameter = []
    for name in fnames:
        pname = name.split(os.sep)[-1].split('amp')[1].split('G')[0]
        try:
            parameter.index(pname)
        except ValueError:
            parameter.append(pname)
    print(parameter)"""

    for datei in dateien:
        amps = []
        freqs = []
        phase = []
        offsets = []

        out, ph, datx, daty = fit_datei(datei, par)

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
    plt.ylabel('Amplitude (XKorr a.u.)')
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

