# coding=utf-8
"""
@author: Valon Lushta
@author: Sebastian Badur
"""

from Module.Abstrakt.Fit import Fit as AbstraktFit
from Module.Signal import signal

from Messwerte import Messwerte


class Fit(AbstraktFit):
    """ Der parallelisierte Fit """
    def __init__(self, laden, par):
        """
        :type laden: Module.Spektroskopie.Laden.GuiSpektrLaden
        :type par: Module.Spektroskopie.Parameter.Parameter
        """
        AbstraktFit.__init__(self, laden, par)
        self.messwerte = None
        """ :type: Messwerte.Messwerte """
        self.anzahl = len(Messwerte.glob_amp(par.verzeichnis))

    def impl_fit(self):
        for reihe in self.messwerte.alle():
            for dc in range(len(reihe.dc)):  # Indizes zu den bestimmten DC-Werten

                amp, phase = self.fit(reihe.amp_freq[dc], reihe.phase_freq[dc])

                # Amplitude auswerten:
                reihe.amp_dc[dc] = amp.best_values['amp']
                reihe.resfreq_dc[dc] = amp.best_values['resfreq']

                # Phase auswerten:
                reihe.phase_dc[dc] = phase.mit_versatz

                self.signal_weiter()

    def lade_messwerte(self):
        self.messwerte = Messwerte(self.par, self.signal_weiter)

    def speichern(self, wohin):
        """
        :type wohin: str
        """
        self.messwerte.speichern(wohin)
