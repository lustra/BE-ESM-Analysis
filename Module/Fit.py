# coding=utf-8
"""
@author: Valon Lushta
@author: Sebastian Badur
"""

import numpy as np
import time
from PyQt4 import QtCore

from Module.FitFunktionen import FitZeile
from Module.Messwerte import Messwerte
from Module.Ergebnis import Ergebnis
from Module.Signal import signal
from Module.Sonstige import Fehler


class Fit(QtCore.QThread):
    """
    Die parallelisierte, statische Fit-Klasse.
    Vor dem Start ist noch das Attribut par mit den Fitparametern zu befüllen und die Qt-Signale zu verbinden.
    """
    def __init__(self):
        QtCore.QThread.__init__(self)
        self.weiter = True
        self.par = None
        self.messwerte = None
        self.av_iter = 0
        self.laufzeit = 0
        self.start_time = 0
        self.erg = None

    def run(self):
        self.weiter = True
        self.start_time = time.time()
        # Messwerte laden
        try:
            self.messwerte = Messwerte(self.par)
            self.emit(signal.importiert)
        except Fehler as f:
            self.emit(signal.fehler, f)
            return

        # p0 = Initial guess
        p0 = np.array([(self.par.fmax - self.par.fmin) / 2 + self.par.fmin, 0.1, 5], dtype=np.double)

        norm = len(self.messwerte.amplitude) - len(p0)

        fitparameter = np.ones((self.par.pixel, self.par.pixel, 3))
        error_fitparameter = np.ones((self.par.pixel, self.par.pixel, 3))
        sphase = np.ones((self.par.pixel, self.par.pixel))  # single phase point off resonance
        iterationen = np.ones((self.par.pixel, self.par.pixel))

        def weitere_zeile(z):
            fitparameter[z.y] = z.fitparameter
            error_fitparameter[z.y] = z.error_fitparameter
            sphase[z.y] = z.sphase
            iterationen[z.y] = z.iterationen
            self.emit(signal.weiter)

        """# Multi-Processing, aber Vorsicht: jeder Prozess arbeitet zwangsweise mit seiner eigenen Speicherkopie
        pool = QtCore.QThreadPool()
        QtCore.QObject.connect(pool, signal.weiter, weitere_zeile)
        for y in range(self.par.pixel):
            if self.weiter:
                while not pool.tryStart(
                    # Eine Zeile fitten
                    FitZeile(self.emit, self.messwerte, p0, norm, y)
                ):
                    pass
        pool.waitForDone()"""

        # Single-Processing
        for y in range(self.par.pixel):
            if self.weiter:
                zeile = FitZeile(self.messwerte, p0, norm, y)
                zeile.run()
                weitere_zeile(zeile)
            else:
                break

        # Fitprozess abschließen ##########
        self.erg = Ergebnis(fitparameter, error_fitparameter, sphase)

        self.av_iter = int(np.average(iterationen))
        self.laufzeit = time.time() - self.start_time

        if self.weiter:
            self.emit(signal.fertig)

    def abbruch(self):
        self.weiter = False
