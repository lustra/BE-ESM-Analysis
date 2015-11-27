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
from Module.Spektroskopie.Messreihe import *


class Messwerte(Messreihe):
    def __init__(self, par):
        """
        :type par: Module.Spektroskopie.Parameter.Parameter
        """
        Messreihe.__init__(self)
        self.omega = self._get

        self.par = par

        if par.messpunkte + par.bereich_rechts <= par.bereich_links or par.bereich_links < 0:
            raise Fehler(IndexError())
        self.frequenzen = np.arange(par.fmin, par.fmax, par.df)
        # Begrenzung des Frequenzbereichs:
        if par.bereich_rechts == 0:
            self.frequenzen = self.frequenzen[par.bereich_links:]
        else:
            self.frequenzen = self.frequenzen[par.bereich_links:par.bereich_rechts]

        dateien = glob(self.par.verzeichnis + 'amp*.tdms')
        for dat_amp in dateien:

            name = dat_amp.split(os.sep + 'amp')[-1].split('w')
            omega = int(name[0])
            name = name[1].split('G')
            ac = name[0]
            dc = name[1].rstrip('V.tdms')

            dat_phase = self.par.verzeichnis + 'phase' + str(omega) + 'w' + ac + 'G' + dc + 'V.tdms'

            amplitude = self.lade_tdms(dat_amp)
            phase = self.lade_tdms(dat_phase)

            self.add(omega, ac, dc, amplitude, phase)

    def lade_tdms(self, datei):
        """
        :type datei: str
        :return: Die gemittelten Messwerte aus der angegebenen Datei
        """
        tdms = TdmsFile(datei).object('Unbenannt', 'Untitled')
        # Beschnittene Daten (links: positiv, rechts: negativ)
        daten = np.zeros(self.par.messpunkte - self.par.bereich_links + self.par.bereich_rechts)
        index_fehler = False
        for mittelung in range(self.par.mittelungen):
            try:
                """
                Mittelung (durch Addition)
                UND
                Begrenzung des Fitbereichs (zur Eliminierung von parasitären Frequenzpeaks) nach Angabe in GUI
                """
                daten += tdms.data[mittelung + self.par.bereich_links:
                                   mittelung + self.par.messpunkte + self.par.bereich_rechts]
            except IndexError:
                """
                In diesem Fall ist ein Messfehler aufgetreten. Das kann (sehr selten) passieren, weshalb der Fit
                dennoch funktionieren muss. Hier ist dann aber ein Einbruch in der Amplitude zu verzeichnen.
                """
                if not index_fehler:
                    index_fehler = True
                    print('Fehlende Messwerte in Datei ' + datei)
        return daten

    def add(self, omega, ac, dc, amplitude, phase):
        if omega not in self._param:
            self._param.append(omega)
            self._reihe.append(Omega(omega))

        zgr = self.omega(omega)
        """ @type: Omega """

        if ac not in zgr._param:
            zgr._param.append(ac)
            zgr._reihe.append(AC(omega, ac))

        zgr = zgr.ac(ac)
        """ @type: AC """
        zgr.dc.append(dc)
        zgr.amp_freq.append(amplitude)
        zgr.phase_freq.append(phase)
