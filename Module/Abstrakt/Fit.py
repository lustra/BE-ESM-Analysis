# coding=utf-8
"""
@author: Valon Lushta
@author: Sebastian Badur
"""

from sys import maxint
import time
import numpy as np
from PyQt4 import QtCore
from scipy.signal import savgol_filter
from lmfit import Model, Parameters

from Module.Signal import signal
from Module.Sonstige import Fehler


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
        """ :type: bool """
        self.av_iter = 0
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

        self.impl_fit()

        self.laufzeit = time.time() - self.start_time

        if self.weiter:
            self.emit(signal.fertig)

    def fit(self, amplitude, phase):
        """
        :type amplitude: numpy.multiarray.ndarray
        :type phase: numpy.multiarray.ndarray
        :rtype: lmfit.model.ModelResult, lmfit.model.ModelResult
        """
        par = self.par
        """ :type: Module.Abstrakt.Parameter.Parameter """

        amplitude = self.filter(amplitude)
        index_max = np.argmax(amplitude)
        start_freq = self.messwerte.frequenzen[index_max]
        start_amp = amplitude[index_max]
        start_off = amplitude[0]  # Erster betrachteter Wert ist bereits eine gute Näherung für den Untergrund

        # Fitparameter für die Fitfunktion
        params = Parameters()
        params.add('resfreq', value=start_freq, min=par.fmin, max=par.fmax)
        params.add('amp', value=start_amp, min=par.amp_min, max=par.amp_max)
        params.add('guete', value=0.5*(par.guete_max+par.guete_min), min=par.guete_min, max=par.guete_max)
        params.add('off', value=start_off, min=par.off_min, max=par.off_max)

        mod = Model(par.fitfunktion)
        erg = mod.fit(
            data=amplitude,
            freq=self.messwerte.frequenzen,
            params=params,
            fit_kws={
                'ftol': 1e-9,
                'xtol': 1e-9,
                'gtol': 1e-9,
                'maxfev': maxint,
                'factor': 0.1
            }
        )

        ph = phase_ermitteln(
            phase_freq=phase,
            resfreq=int((erg.best_values['resfreq'] - par.fmin) / par.df),
            versatz=par.phase_versatz,
            modus=par.phase_modus,
            savgol=self.filter
        )

        return erg, ph

    def filter(self, daten):
        """
        :type daten: numpy.multiarray.ndarray
        :return: Der mittels Savitzky-Golay-Methode geglätte Verlauf
        :rtype: numpy.multiarray.ndarray
        """
        return savgol_filter(daten, self.par.fenster, self.par.ordnung)

    def abbruch(self):
        self.weiter = False

    def lade_messwerte(self):
        raise NotImplementedError()

    def impl_fit(self):
        raise NotImplementedError()

    def speichern(self, wohin):
        raise NotImplementedError()
