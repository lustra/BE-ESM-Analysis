# coding=utf-8
import numpy as np
from lmfit.models import * #### alternatives Fitten siehe https://lmfit.github.io/lmfit-py/
import matplotlib.pyplot as plt
from glob import glob
from nptdms import TdmsFile





def read_tdmsfile(folder): # Dateiname aufgeteilt und Nummerisch sortiert
    tdms_file = TdmsFile(folder)
    channel = tdms_file.object('Unbenannt', 'Untitled')     # erster Name ist der Gruppenname dann der Kanalname
    multy = np.array(channel.data)
    datay = np.zeros(500)

    for n in range(100):
        for m in range(500):
            datay[m] += multy[m+n*500]

    datay = datay[50:450]
    datax = range(62000, 72000, 20)[50:450]

    return datax, datay




def resonance_lorentz(freq, resfreq, amp, guete, off):
    return amp * resfreq**2 / (
        guete * np.sqrt((freq**2 - resfreq**2)**2 + (freq * resfreq / guete)**2)
    ) + off

mod = Model(resonance_lorentz)




duplicate = []
offsets = []
erg_amp = []
erg_freq = []
erg_phase = []

folder = "/home/sebadur/Dokumente/BE-Spektroskopie/2015-11-10 Vergleich/"

amps = []
freqs = []
phase = []
fnames = glob(folder+"amp1w8*.tdms")    # alle dateien in diesem Ordner mit der Endung txt
sorted_fnames = sorted(
    fnames, key=lambda x: int(float(x.split('/')[-1].split('.')[0].split('G')[1].replace(',', '.').split('V')[0])*10)
)
for name in sorted_fnames:
    datx, daty = read_tdmsfile(name)
    phasx, phasy = read_tdmsfile(name.replace('amp1w8', 'phase1w8'))  # DAS KANN SO NICHT BLEIBEN (ersetzt nicht nur im Dateinamen, sondern auch im Pfad)

    index_max = np.argmax(daty)
    start_freq = datx[index_max]
    start_amp = daty[index_max]
    start_off = daty[0]

    out = mod.fit(daty, freq=datx, resfreq=start_freq, amp=start_amp, guete=10, off=start_off, verbose=False)

    if name in ["/home/sebadur/Dokumente/BE-Spektroskopie/2015-11-10 Vergleich/amp1w8,000000G-2,000000V.tdms",
                "/home/sebadur/Dokumente/BE-Spektroskopie/2015-11-10 Vergleich/amp1w8,000000G-1,000000V.tdms",
                "/home/sebadur/Dokumente/BE-Spektroskopie/2015-11-10 Vergleich/amp1w8,000000G0,000000V.tdms",
                "/home/sebadur/Dokumente/BE-Spektroskopie/2015-11-10 Vergleich/amp1w8,000000G1,000000V.tdms"] and True:
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



for i in range(1):
    plt.plot(offsets, erg_amp[i], '.')
plt.legend(loc=9)
plt.ylabel('Amplitude (FFT a.u.)')
plt.xlabel('Offset (V)')
plt.show()

for i in range(1):
    plt.plot(offsets, erg_freq[i], '.')
plt.legend(loc=9)
plt.ylabel('Resonanzfrequenz (Hz)')
plt.xlabel('Offset (V)')
plt.show()

for i in range(1):
    plt.plot(offsets, erg_phase[i], '.')
plt.legend(loc=9)
plt.ylabel('Phase (Grad)')
plt.xlabel('Offset (V)')
plt.show()

print 'finished!'

