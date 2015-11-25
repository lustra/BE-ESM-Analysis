# coding=utf-8
"""
@author: Valon Lushta
@author: Sebastian Badur
"""

import os
import numpy as np
from nptdms import TdmsFile
from glob import glob

from Module.Sonstige import Fehler


class Messwerte:
    def __init__(self, par):
        """
        :type par: Module.Spektroskopie.Parameter.Parameter
        """
        self.par = par
        self.frequenzen = np.arange(par.fmin, par.fmax, par.df)
        # Begrenzung des Frequenzbereichs:
        self.frequenzen = self.frequenzen[par.bereich_links:par.bereich_rechts]

        self.messreihe = [[[]]]

        dateien = glob(self.par.verzeichnis + 'amp*.tdms')
        for datei in dateien:
            tdms = TdmsFile(datei).object('Unbenannt', 'Untitled')
            amplituden = np.zeros(par.messpunkte)

            for mittelung in range(par.mittelungen):
                for messpunkt in range(par.messpunkte):
                    try:
                        amplituden[messpunkt] += tdms.data[messpunkt + mittelung * par.messpunkte]
                    except IndexError:
                        """
                        In diesem Fall ist ein Messfehler aufgetreten. Das kann (sehr selten) passieren, weshalb der Fit
                        dennoch funktionieren muss. Hier ist dann aber ein Einbruch in der Amplitude zu verzeichnen.
                        """
                        break

            if len(amplituden) + par.bereich_rechts <= par.bereich_links or par.bereich_links < 0:
                raise Fehler(IndexError())
            elif par.bereich_rechts == 0:
                par.bereich_rechts = len(amplituden)

            # Begrenzung des Fitbereichs (zur Eliminierung von parasitären Frequenzpeaks) nach Angabe in GUI
            amplituden = amplituden[par.bereich_links:par.bereich_rechts]

            name = datei.split(os.sep + 'amp')[-1].replace(',', '.').split('w')
            omega = int(name[0])
            name = name[1].split('G')
            ac = float(name[0])
            dc = float(name[1].rstrip('V.tdms'))

            self.messreihe[omega][ac][dc] = amplituden


        #return datax, datay
