# coding=utf-8
"""
@author: Valon Lushta
@author: Sebastian Badur
"""

import numpy as np
import time
from PyQt4 import QtCore
from multiprocessing import Process, cpu_count
from pathos.multiprocessing import Pool

from Module.FitZeile import FitZeile
from Module.Messwerte import Messwerte
from Module.Ergebnis import Ergebnis
from Module.Signal import signal
from Module.Sonstige import Fehler


class Fit(QtCore.QThread):
    """
    Die parallelisierte, statische Fit-Klasse.
    Vor dem Start sind noch die Messwerte zu setzen, das Attribut par mit den Fitparametern zu befüllen
    und die Qt-Signale zu verbinden.
    """
    def __init__(self):
        QtCore.QThread.__init__(self)
        self.weiter = True
        """ @type: bool """
        self.par = None
        """ @type: Module.Sonstige.Parameter """
        self.messwerte = None
        """ @type: Module.Messwerte.Messwerte """
        self.av_iter = 0
        self.laufzeit = 0
        self.start_time = 0
        self.erg = None
        """ @type: Module.Ergebnis.Ergebnis """

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

        # Multi-Prozessierung ##########
        """zeilen = Pool().map(
            FitZeile(self.messwerte, p0, norm).fitten,
            range(self.par.pixel)
        )

        for z in zeilen:
            fitparameter[z.y] = z.fitparameter
            error_fitparameter[z.y] = z.error_fitparameter
            sphase[z.y] = z.sphase
            iterationen[z.y] = z.iterationen"""

        kerne = cpu_count()
        zeile = [None] * kerne
        prozess = [None] * kerne

        for start in range(0, self.par.pixel, kerne):
            if start + kerne < self.par.pixel:
                pool = range(kerne)
            else:
                pool = range(self.par.pixel - start)

            # Einige Fit-Prozesse starten
            for n in pool:
                zeile[n] = FitZeile(self.messwerte, p0, norm, y=start+n)
                prozess[n] = Process(target=zeile[n].run)
                prozess[n].start()

            # Fertige Fits auswerten
            for n in pool:
                y = zeile[n].y
                prozess[n].join()
                fitparameter[y] = zeile[n].fitparameter
                error_fitparameter[y] = zeile[n].error_fitparameter
                sphase[y] = zeile[n].sphase
                iterationen[y] = zeile[n].iterationen
                self.emit(signal.weiter)

            if not self.weiter:
                break

        # Fitprozess abschließen ##########
        self.erg = Ergebnis(fitparameter, error_fitparameter, sphase)

        self.av_iter = int(np.average(iterationen))
        self.laufzeit = time.time() - self.start_time

        if self.weiter:
            self.emit(signal.fertig)

    def abbruch(self):
        self.weiter = False
