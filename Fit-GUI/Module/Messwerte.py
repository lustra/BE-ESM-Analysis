# coding=utf-8
import numpy as np
from nptdms import TdmsFile
from glob import glob

from ResonanzFit import lang
from Module.Sonstige import Fehler
from Module.Strings import *


class Messwerte:
    """ Werte der Amplitude und Phase für jeden Pixel einer Messung """
    def __init__(self, par):
        self.par = par
        self.amplitude, self.amplitude_namen = lade_tdms(par, "amp")
        self.phase, self.phase_namen = lade_tdms(par, "phase")

        if par.pixel != len(self.amplitude[0]) / par.messpunkte:
            raise Fehler(mw_pixelzahl[lang])

        # Definition der Frequenz:
        self.frequenzen = np.arange(
            par.fmin, par.fmax,
            float((par.fmax - par.fmin) / float(par.messpunkte))  # delta f
        )

    def amplituden(self, y):
        return split_list(
            np.array(np.multiply(self.amplitude[y], 100), dtype=np.double),
            wanted_parts=self.par.pixel
        )

    def phasen(self, y):
        return split_list(
            np.array(self.phase[y], dtype=np.double),
            wanted_parts=self.par.pixel
        )


def lade_tdms(par, typ):
    daten = []
    fnames = glob(par.verzeichnis.__str__() + typ + "*.tdms")  # alle Dateien in diesem Ordner mit der Endung TDMS
    # Dateiname aufteilen und numerisch sortieren:
    sorted_fnames = sorted(fnames, key=lambda x: int(x.split('/')[-1].split(typ)[1].split('.')[0]))
    if len(sorted_fnames) == 0:
        raise Fehler(mw_tdms[lang])

    for i in range(par.pixel):
        tdms_file = TdmsFile(sorted_fnames[i])
        channel = tdms_file.object("Unbenannt", "Untitled")  # erster Name ist der Gruppenname, dann der Kanalname
        daten.append(np.array(channel.data))
    return daten, [fn.split('/')[-1] for fn in sorted_fnames]


def split_list(alist, wanted_parts=1):
    length = len(alist)
    return [alist[i * length // wanted_parts: (i + 1) * length // wanted_parts]
            for i in range(wanted_parts)]
