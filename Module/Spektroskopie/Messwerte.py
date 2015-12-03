# coding=utf-8
"""
@author: Valon Lushta
@author: Sebastian Badur
"""

import os
import numpy as np
from bisect import bisect_left
from nptdms import TdmsFile
from glob import glob

from Module.Abstrakt.Messwerte import Messwerte as AbstraktMesswerte
from Module.Sonstige import Fehler, punkt
from Module.Spektroskopie.Messreihe import *


class Messwerte(AbstraktMesswerte, Messreihe):
    def __init__(self, par, signal_weiter):
        """
        :type par: Module.Spektroskopie.Parameter.Parameter
        :type signal_weiter: () -> None
        """
        AbstraktMesswerte.__init__(self, par)
        Messreihe.__init__(self)
        self.omega = self._get
        """ @type: (int) -> Omega """
        self.anzahl_messreihen = 0

        if par.messpunkte + par.bereich_rechts <= par.bereich_links or par.bereich_links < 0:
            raise Fehler(IndexError())
        self.frequenzen = np.arange(par.fmin, par.fmax, par.df)
        # Begrenzung des Frequenzbereichs:
        if par.bereich_rechts == 0:
            self.frequenzen = self.frequenzen[par.bereich_links:]
        else:
            self.frequenzen = self.frequenzen[par.bereich_links:par.bereich_rechts]

        dateien = Messwerte.glob_amp(self.par.verzeichnis)
        for dat_amp in dateien:

            name = dat_amp.split(os.sep + 'amp')[-1].split('w')
            omega = int(name[0])
            name = name[1].split('G')
            ac = name[0]
            dc = name[1].rstrip('V.tdms')

            dat_phase = self.par.verzeichnis + 'phase' + str(omega) + 'w' + ac + 'G' + dc + 'V.tdms'

            amplitude = self.lade_tdms(dat_amp)
            phase = self.lade_tdms(dat_phase)

            self.add(omega, punkt(ac), punkt(dc), amplitude, phase)

            self.amplitude_namen.append(dat_amp.split(os.sep)[-1])
            self.phase_namen.append(dat_phase.split(os.sep)[-1])
            signal_weiter()

    @staticmethod
    def glob_amp(verzeichnis):
        return glob(verzeichnis + 'amp*.tdms')

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
                start = mittelung * self.par.messpunkte
                links = start + self.par.bereich_links
                rechts = start + self.par.messpunkte + self.par.bereich_rechts
                daten += tdms.data[links:rechts]
            except (ValueError, IndexError):
                """
                In diesem Fall ist ein Messfehler aufgetreten. Das kann (sehr selten) passieren, weshalb der Fit
                dennoch funktionieren muss. Hier ist dann aber ein Einbruch in der Amplitude zu verzeichnen.
                """
                if not index_fehler:
                    index_fehler = True
                    print('Fehlende Messwerte in Datei ' + datei)
        return daten

    def add(self, omega, ac, dc, amplitude, phase):
        """
        :type omega: int
        :type ac: float
        :type dc: float
        :type amplitude: numpy.multiarray.ndarray
        :type phase: numpy.multiarray.ndarray
        """
        if omega not in self._param:
            index = bisect_left(self._param, omega)
            self._param.insert(index, omega)
            self._reihe.insert(index, Omega(omega))

        zgr = self.omega(omega)
        if ac not in zgr._param:
            index = bisect_left(zgr._param, ac)
            zgr._param.insert(index, ac)
            zgr._reihe.insert(index, AC(omega, ac))

        zgr = zgr.ac(ac)
        """ @type: AC """
        index = bisect_left(zgr.dc, dc)  # Sortiert einfügen
        zgr.dc.insert(index, dc)
        zgr.amp_freq.insert(index, amplitude)
        zgr.phase_freq.insert(index, phase)

        self.anzahl_messreihen += 1

    def str_omegas(self):
        return [str(omega) for omega in self._param]

    def str_acs(self, omega):
        """
        :type omega: int
        """
        return [str(ac) for ac in self.omega(omega)._param]

    def str_dcs(self, omega, ac):
        """
        :type omega: int
        :type ac: float
        """
        return [str(dc) for dc in self.omega(omega).ac(ac).dc]

    def speichern(self, wohin):
        """
        :type wohin: str
        """
        reihen = self.alle()
        """for reihe in reihen:
            # Sortieren nach DC (weil die Daten beim ersten Speichern noch ungeordnet vorliegen)
            abh_dc = zip(reihe.dc, reihe.amp_dc, reihe.resfreq_dc, reihe.phase_dc)
            abh_dc.sort()
            reihe.dc, reihe.amp_dc, reihe.resfreq_dc, reihe.phase_dc = zip(*abh_dc)"""

        datei_speichern(wohin + '.amp', reihen, 'Amp. (bel.)', lambda r, n: str(r.amp_dc[n]))
        datei_speichern(wohin + '.freq', reihen, 'Resfreq. (kHz)', lambda r, n: str(r.resfreq_dc[n]))
        datei_speichern(wohin + '.phase', reihen, 'Phase (Grad)', lambda r, n: str(r.phase_dc[n]))


def datei_speichern(wohin, reihen, bezeichnung, messwert):
    """
    :type wohin: str
    :type reihen: list[AC]
    :type bezeichnung: str
    :type messwert: (AC, int) -> str
    """
    datei = open(wohin, 'w')

    zeile = 'DC/V'
    for reihe in reihen:
        zeile += '\t' + bezeichnung + ' bei ' + str(reihe.omega) + ' omega, ' + str(reihe.ac) + ' AC/V'
    datei.write(zeile + '\n')

    # Jetzt muss angenommen werden, dass für alle Messreihen gleiche DC-Werte vorliegen
    for dc_index in range(len(reihen[0].dc)):
        zeile = str(reihen[0].dc[dc_index])
        for reihe in reihen:
            zeile += '\t' + messwert(reihe, dc_index)
        datei.write(zeile + '\n')

    datei.close()
