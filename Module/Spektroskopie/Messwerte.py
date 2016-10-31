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

from Messreihe import *


amp_pre = 'amp'
phase_pre = ''  # Muss nicht stimmen


class Messwerte(AbstraktMesswerte, Messreihe):
    def __init__(self, par, signal_weiter):
        """
        :type par: Module.Spektroskopie.Parameter.Parameter
        :type signal_weiter: () -> None
        """
        AbstraktMesswerte.__init__(self, par)
        Messreihe.__init__(self)
        self.omega = self._get
        """ :type: (int) -> Omega """
        self.anzahl_messreihen = 0

        if par.messpunkte + par.bereich_rechts <= par.bereich_links or par.bereich_links < 0:
            raise Fehler(IndexError())
        self.frequenzen = np.arange(par.fmin, par.fmax, par.df)
        # Begrenzung des Frequenzbereichs:
        if par.bereich_rechts == 0:
            self.frequenzen = self.frequenzen[par.bereich_links:]
        else:
            self.frequenzen = self.frequenzen[par.bereich_links:par.bereich_rechts]

        datei = self.par.datei  # '/home/sebadur/Dokumente/BaTiO3/2016-10-26/+30V/16-10-26-15-15-09.tdms'
        kanal = 'elstat'

        omega = 1
        amplitude = TdmsFile(datei).channel_data(kanal, 'amp') * 1000  # V -> mV
        phase = TdmsFile(datei).channel_data(kanal, 'phase')
        xf = (self.par.fmax - self.par.fmin) / self.par.df
        for u in range(len(amplitude)/xf):
            links = u * xf + self.par.bereich_links
            rechts = (u + 1) * xf + self.par.bereich_rechts
            self.add(omega, 1., u, amplitude[links:rechts], phase[links:rechts])
            self.amplitude_namen.append('debug')
            self.phase_namen.append('debug')
            signal_weiter()

    def lade_tdms(self, datei, kanal='Untitled'):
        """
        :type datei: str
        :return: Die gemittelten Messwerte aus der angegebenen Datei
        :rtype: numpy.mutliarray.ndarray
        """
        # Beschnittene Daten (links: positiv, rechts: negativ)
        daten = np.zeros(self.par.messpunkte - self.par.bereich_links + self.par.bereich_rechts)
        try:
            tdat = TdmsFile(datei)
            # tdms = tdat.object(tdat.groups()[0], kanal)
            tdms = tdat.object('elstat', kanal)
        except (ValueError, IOError):
            print('Datei ' + datei + ' nicht auslesbar')
            return daten
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

                """if mittelung == 0:
                    name = raw_input('$')
                    import matplotlib.pyplot as plt
                    plt.title(name+ ": Einzelmessung")
                    plt.xlabel(u"Frequenz / Hz")
                    plt.ylabel(u"Amplitude / µV")
                    plt.plot(
                        self.frequenzen,
                        daten * (1000*1000/50/2.9),
                        antialiased=True
                    )
                    plt.show()
                elif mittelung == self.par.mittelungen-1:
                    name = raw_input('$')
                    import matplotlib.pyplot as plt
                    plt.title(name+ ": 200x gemittelt")
                    plt.xlabel(u"Frequenz / Hz")
                    plt.ylabel(u"Amplitude / µV")
                    plt.plot(
                        self.frequenzen,
                        daten / self.par.mittelungen * (1000*1000/180),
                        antialiased=True
                    )
                    plt.show()"""

            except (ValueError, IndexError):
                """
                In diesem Fall ist ein Messfehler aufgetreten. Das kann (sehr selten) passieren, weshalb der Fit
                dennoch funktionieren muss. Hier ist dann aber ein Einbruch in der Amplitude zu verzeichnen.
                """
                if not index_fehler:
                    index_fehler = True
                    print('Fehlende Messwerte in Datei ' + datei)
        return daten / self.par.mittelungen

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
        """ :type: AC """
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
        # TODO derzeit nur ein AC:
        fit = self.alle()[0]

        datei = open(wohin, 'w')
        for n in range(len(fit.dc)):
            datei.write(
                str(fit.dc[n]) + ',' + str(fit.amp_dc[n]) + ',' + str(fit.amp_fhlr_dc[n]) + ',' +
                str(fit.resfreq_dc[n]) + ',' + str(fit.resfreq_fhlr_dc[n]) + ',' + str(fit.guete[n]) + ',' +
                str(fit.guete_fhlr[n]) + ',' + str(fit.phase_dc[n]) + '\n'
            )
        datei.close()

"""
def datei_speichern(wohin, reihen, bezeichnung, messwert):
    ""
    :type wohin: str
    :type reihen: list[AC]
    :type bezeichnung: str
    :type messwert: (AC, int) -> str
    ""
    datei = open(wohin, 'w')

    zeile = 'DC/V'
    for reihe in reihen:
        zeile += '\t' + bezeichnung + ' bei ' + str(reihe.omega) + ' omega, ' + str(reihe.ac) + ' AC/V'
    datei.write(zeile + '\n')

    # Jetzt muss angenommen werden, dass für alle Messreihen gleiche DC-Werte vorliegen
    for dc_index in range(len(reihen[0].dc)):
        zeile = str(reihen[0].dc[dc_index])
        for reihe in reihen:
            try:
                zeile += '\t' + messwert(reihe, dc_index)
            except IndexError:
                pass
        datei.write(zeile + '\n')

    datei.close()
"""
