# coding=utf-8
"""
@author: Valon Lushta
@author: Sebastian Badur
"""

import numpy as np
from scipy.signal import savgol_filter

from lmfit import Model, Parameters

from Module.Abstrakt.Fit import Fit as AbstraktFit
from Module.Spektroskopie.Messwerte import Messwerte
from Module.Phase import phase_ermitteln
from Module.Signal import signal


class Fit(AbstraktFit):
    """ Der parallelisierte Fit """
    def __init__(self, laden, par):
        """
        :type laden: Module.Spektroskopie.Laden.GuiSpektrLaden
        :type par: Module.Spektroskopie.Parameter.Parameter
        """
        AbstraktFit.__init__(self, laden, par)
        self.messwerte = None
        """ @type: Module.Spektroskopie.Messwerte.Messwerte """

    def impl_fit(self):
        for reihe in self.messwerte.alle():
            for dc in range(len(reihe.dc)):  # Indizes zu den bestimmten DC-Werten

                erg, phase = self.fit(reihe.amp_freq[dc], reihe.phase_freq[dc])
                reihe.amp_dc.append(erg.best_values['amp'])
                reihe.resfreq_dc.append(erg.best_values['resfreq'])
                reihe.phase_dc.append(phase)

                #erg.infodict.get("nfev")
                self.signal_weiter()

        self.av_iter = 0

    def signal_weiter(self):
        self.emit(signal.weiter)

    def lade_messwerte(self):
        self.messwerte = Messwerte(self.par, self.signal_weiter)

    def fit(self, amplitude, phase):
        """
        :type amplitude: numpy.multiarray.ndarray
        :type phase: numpy.multiarray.ndarray
        :returns: lmfit.model.ModelResult, float
        """
        par = self.par
        """ @type: Module.Spektroskopie.Parameter.Parameter """

        amplitude = self.filter(amplitude)
        index_max = np.argmax(amplitude)
        start_freq = self.messwerte.frequenzen[index_max]
        start_amp = amplitude[index_max]
        start_off = amplitude[0]  # Erster betrachteter Wert ist bereits eine gute Näherung für den Untergrund

        # Fitparameter für die Fitfunktion
        params = Parameters()
        params.add('resfreq', value=start_freq, min=par.fmin, max=par.fmax)
        params.add('amp', value=start_amp, min=par.amp_min, max=par.amp_max)
        params.add('guete', value=par.guete, min=par.guete_min, max=par.guete_max)
        params.add('off', value=start_off, min=par.off_min, max=par.off_max)

        mod = Model(par.fitfunktion)
        erg = mod.fit(
            data=amplitude,
            freq=self.messwerte.frequenzen,
            params=params
        )

        neben_resfreq = int((erg.best_values['resfreq'] - par.fmin) / par.df) + par.phase_versatz
        neben_resfreq = max(min(neben_resfreq, len(phase)-1), 0)  # Bereichsüberschreitung verhindern
        ph = self.filter(phase)[neben_resfreq] / par.mittelungen

        """ph = phase_ermitteln(
            phase_freq=phase / par.mittelungen,
            resfreq=int((erg.best_values['resfreq'] - par.fmin) / par.df),
            versatz=par.phase_versatz,
            filter_fkt=self.filter
        )"""

        return erg, ph

    def filter(self, daten):
        """
        :type daten: numpy.multiarray.ndarray
        :return: Der mittels Savitzky-Golay-Methode geglätte Verlauf
        :returns: numpy.multiarray.ndarray
        """
        return savgol_filter(daten, self.par.fenster, self.par.ordnung)

    def speichern(self, wohin):
        """
        :type wohin: str
        """
        self.messwerte.speichern(wohin)
