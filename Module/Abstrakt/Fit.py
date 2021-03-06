# coding=utf-8
"""
@author: Valon Lushta
@author: Sebastian Badur
"""

import time
import numpy as np
from PyQt4 import QtCore
from scipy.signal import savgol_filter
from lmfit import Parameters

from Module.Signal import signal
from Module.Sonstige import Fehler, Abbruch, Nichts, int_max


fit_genauigkeit = {
    'ftol': 1e-9,  # Geringe Toleranzen
    'xtol': 1e-9,
    'gtol': 1e-9,
    'maxfev': int_max,  # Maximale Iterationsanzahl
    'factor': 0.1  # Kleinster möglicher Schrittwert für die leastsq-Methode
}


class Fit(QtCore.QThread):
    """
    Die parallelisierte, statische, abstrakte Fit-Klasse.
    Vor dem Start sind noch die Messwerte zu setzen, das Attribut par mit den Fitparametern zu befüllen
    und die Qt-Signale zu verbinden.
    """
    def __init__(self, laden, par):
        """
        :type laden: Module.Abstrakt.Laden.GuiAbstraktLaden
        :type par: Module.Abstrakt.Parameter.Parameter
        """
        QtCore.QThread.__init__(self)
        self.laden = laden
        self.par = par
        self.weiter = True
        self.laufzeit = 0
        self.start_time = 0

        QtCore.QObject.connect(self, signal.importiert, self.laden.app.importiert)
        QtCore.QObject.connect(self, signal.fehler, self.laden.fehler)
        QtCore.QObject.connect(self, signal.weiter, self.laden.mehr_fortschritt)
        QtCore.QObject.connect(self, signal.fertig, self.laden.fit_fertig)

    def run(self):
        self.weiter = True
        self.start_time = time.time()

        # Messwerte laden
        try:
            self.lade_messwerte()
            self.emit(signal.importiert)
        except Fehler as f:
            self.emit(signal.fehler, f)
            return
        except Abbruch:
            return

        self.impl_fit()

        self.laufzeit = time.time() - self.start_time

        if self.weiter:
            self.emit(signal.fertig)

    debug_schnell = False
    konsole = False

    def fit(self, amplitude, phase):
        """
        :type amplitude: numpy.multiarray.ndarray
        :param phase: Phase in Abhängigkeit der Frequenz in Grad
        :type phase: numpy.multiarray.ndarray
        :return: Gefittete Amplitude und gefittete oder geglättete Phase im Bereich um Resonanzfrequenz +/- Versatz
        :rtype: ModelResult, ModelResult
        """
        par = self.par

        # ----------------------------------------
        # ----------- AMPLITUDE fitten -----------
        # ----------------------------------------

        amplitude = self.filter(amplitude)
        index_max = np.argmax(amplitude)
        start_freq = self.messwerte.frequenzen[index_max]
        start_amp = amplitude[index_max]
        start_off = amplitude[0]  # Erster betrachteter Wert ist bereits eine gute Näherung für den Untergrund

        # Fitparameter für die Fitfunktion
        par_amp = Parameters()
        par_amp.add('resfreq', value=start_freq, min=par.fmin, max=par.fmax)
        par_amp.add('amp', value=start_amp, min=par.amp_min, max=par.amp_max)
        par_amp.add('guete', value=0.5*(par.guete_max+par.guete_min), min=par.guete_min, max=par.guete_max)
        par_amp.add('off', value=start_off, min=par.off_min, max=par.off_max)

        amp = par.mod_amp.fit(
            data=amplitude,
            freq=self.messwerte.frequenzen,
            params=par_amp,
            fit_kws=fit_genauigkeit
        )
        # Resonanzfrequenz
        resfreq = amp.best_values['resfreq']

        if Fit.konsole:
            print(amp.best_values)

        # ----------------------------------------
        # ------------- PHASE fitten -------------
        # ----------------------------------------

        halb = abs(par.phase_versatz) * par.df  # Halbe Frequenzbreite des Phasenversatzes
        von = resfreq - halb  # Untere Versatzgrenze
        bis = resfreq + halb  # Obere Versatzgrenze

        fmin = par.fmin + par.bereich_links * par.df
        fmax = par.fmax + par.bereich_rechts * par.df  # Ist negativ definiert

        if von < fmin:  # Die Resonanzfrequenz liegt zu weit links:
            # Auswahlbereich nach rechts verschieben, aber nicht über den Frequenzbereich hinaus
            bis = min(bis - von + fmin, fmax)
            von = fmin
        elif bis > fmax:  # Die Resonanz lieg zu weit rechts:
            von = max(von - bis + fmax, fmin)  # Verschieben, aber nicht über linken Rand hinaus
            bis = fmax

        # Phase und Frequenz beschneiden
        index_von = self.freq_index(von)
        index_bis = self.freq_index(bis)
        wahl_phase = phase[index_von:index_bis]
        wahl_frequenz = self.messwerte.frequenzen[index_von:index_bis]

        # Fitparameter für die Fitfunktion
        par_ph = Parameters()  # TODO
        par_ph.add('resfreq', value=resfreq, min=von, max=bis)
        par_ph.add('guete', value=3, min=-10, max=10)
        par_ph.add('phase', value=200, min=90, max=425)

        if par.mod_ph is not None:
            ph = par.mod_ph.fit(
                data=wahl_phase,
                freq=wahl_frequenz,
                params=par_ph,
                method='differential_evolution',  # 'cg' passt auch gut
                fit_kws=fit_genauigkeit
            )
        else:
            ph = Nichts()
            ph.best_fit = self.filter(wahl_phase)
            ph.chisqr = 0  # TODO

        # Zusätzliche Informationen für den Phasenfit:
        if par.phase_versatz < 0:
            ph.mit_versatz = ph.best_fit[0]
        elif par.phase_versatz > 0:
            ph.mit_versatz = ph.best_fit[-1]
        else:
            ph.mit_versatz = ph.best_fit[len(ph.best_fit) // 2]
        ph.frequenzen = wahl_frequenz

        return amp, ph

    def freq_index(self, freq):
        return int((freq - self.par.fmin) // self.par.df) - self.par.bereich_links

    def signal_weiter(self):
        if self.weiter:
            self.emit(signal.weiter)
        else:
            raise Abbruch()

    def filter(self, daten):
        """
        :type daten: numpy.multiarray.ndarray
        :return: Der mittels Savitzky-Golay-Methode geglätte Verlauf
        :rtype: numpy.multiarray.ndarray
        """
        return savgol_filter(daten, self.par.fenster, self.par.ordnung)
        # TODO Filtereinstellungen für Phase und Amplitude trennen (bei Phase nur für geglättete Messwerte benötigt)

    def abbruch(self):
        self.weiter = False

    def lade_messwerte(self):
        raise NotImplementedError()

    def impl_fit(self):
        raise NotImplementedError()

    def speichern(self, wohin):
        raise NotImplementedError()
