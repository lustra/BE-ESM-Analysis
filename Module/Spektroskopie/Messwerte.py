# coding=utf-8
"""
@author: Valon Lushta
@author: Sebastian Badur
"""

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

        dateien = glob(self.par.verzeichnis + 'amp*.tdms')
        for datei in dateien:
            tdms = TdmsFile(datei).object('Unbenannt', 'Untitled')
            multy = np.array(tdms.data)
            amplituden = np.zeros(par.messpunkte)

            for mittelung in range(par.mittelungen):
                for messpunkt in range(par.messpunkte):
                    try:
                        amplituden[messpunkt] += multy[messpunkt + mittelung * par.messpunkte]
                    except IndexError:
                        """
                        In diesem Fall ist ein Messfehler aufgetreten. Das kann (sehr selten) passieren, weshalb der Fit
                        dennoch funktionieren muss. Hier ist dann aber ein Einbruch in der Amplitude zu verzeichnen.
                        """
                        break

            anz = len(amplituden)
            if anz + par.bereich_rechts <= par.bereich_links or par.bereich_links < 0:
                raise Fehler(IndexError())
            elif par.bereich_rechts == 0:
                par.bereich_rechts = anz

            # Begrenzung des Fitbereichs (zur Eliminierung von parasitären Frequenzpeaks) nach Angabe in GUI
            amplituden = amplituden[par.bereich_links:par.bereich_rechts]

        #return datax, datay




        self.omega = omega


class Omega:
    def __init__(self, ac):
        """
        :type ac: AC
        """
        self.ac = ac


class AC:
    def __init__(self, dc):
        """
        :type dc: DC
        """
        self.dc = dc


class DC:
    def __init__(self, messung, fit):
        """
        :type messung: numpy.multiarray.ndarray
        :type fit: numpy.multiarray.ndarray
        """
        self.messung = messung
        self.fit = fit
