# coding=utf-8
"""
@author: Valon Lushta
@author: Sebastian Badur
"""

import os
import numpy as np
from nptdms import TdmsFile
from glob import glob

from ResonanzFit import lang
from Module.Sonstige import Fehler
from Module.Strings import *


class Messwerte:
    def __init__(self, par):
        """
        :type par: Module.Sonstige.Parameter
        :return: Werte der Amplitude und Phase für jeden Pixel einer Messung
        """
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
        """
        :type y: numpy.multiarray.ndarray
        """
        return split_list(
            np.array(np.multiply(self.amplitude[y], 100), dtype=np.double),
            wanted_parts=self.par.pixel
        )

    def phasen(self, y):
        """
        :type y: numpy.multiarray.ndarray
        """
        return split_list(
            np.array(self.phase[y], dtype=np.double),
            wanted_parts=self.par.pixel
        )


def lade_tdms(par, typ):
    """
    :type par: Module.Sonstige.Parameter
    :type typ: str
    """
    daten = []
    namen = []

    # Dateinamen aufteilen und numerisch sortieren:
    sorted_fnames = sorted(
        glob(os.path.join(par.verzeichnis, typ + "*.tdms")),  # alle Dateien in diesem Ordner mit der Endung TDMS
        key=lambda x: int(x.split(os.sep)[-1].split(typ)[1].split('.')[0])  # Zeilennummer hinter dem Typnamen
    )

    # Offenbar das falsche Verzeichnis, wenn gar keine TDMS-Dateien gefunden wurden
    if len(sorted_fnames) == 0:
        raise Fehler(mw_tdms[lang])

    verbleibend = par.messpunkte
    for tdms_fname in sorted_fnames:
        if verbleibend != 0:
            verbleibend -= 1
            tdms_file = TdmsFile(tdms_fname)
            channel = tdms_file.object("Unbenannt", "Untitled")  # erster Name ist der Gruppenname, dann der Kanalname
            daten.append(np.array(channel.data))
            namen.append(tdms_fname.split(os.sep)[-1])
        else:
            break

    # Es fehlen Messdaten, die letzte Zeile wird einfach vervielfacht
    while verbleibend > 0:
        verbleibend -= 1
        daten.append(daten[-1])

    return daten, namen


def split_list(alist, wanted_parts=1):
    """
    :type alist: numpy.multiarray.ndarray
    """
    length = len(alist)
    return [alist[i * length // wanted_parts: (i + 1) * length // wanted_parts]
            for i in range(wanted_parts)]
