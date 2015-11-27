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
            channel = tdms_file.object('Unbenannt', 'Untitled')  # erster Name ist der Gruppenname, dann der Kanalname
            daten.append(np.array(channel.data))
            namen.append(tdms_fname.split(os.sep)[-1])
        else:
            break

    # Es fehlen Messdaten, die letzte Zeile wird einfach vervielfacht
    if verbleibend > 0:
        print("Fehlende Messdaten")
        while verbleibend > 0:
            verbleibend -= 1
            daten.append(daten[-1])

    return daten, namen
