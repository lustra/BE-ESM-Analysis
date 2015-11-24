# coding=utf-8
"""
@author: Valon Lushta
@author: Sebastian Badur
"""

import time
from PyQt4 import QtCore

from Module.Signal import signal
from Module.Sonstige import Fehler


class Fit(QtCore.QThread):
    """
    Die parallelisierte, statische, abstrakte Fit-Klasse.
    Vor dem Start sind noch die Messwerte zu setzen, das Attribut par mit den Fitparametern zu befüllen
    und die Qt-Signale zu verbinden.
    """
    def __init__(self):
        QtCore.QThread.__init__(self)
        self.weiter = True
        """ @type: bool """
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
            self.emit(signal.importiert)
            self.lade_messwerte()
        except Fehler as f:
            self.emit(signal.fehler, f)
            return

        self.impl_fit()

        self.laufzeit = time.time() - self.start_time

        if self.weiter:
            self.emit(signal.fertig)

    def lade_messwerte(self):
        raise NotImplementedError()

    def impl_fit(self):
        raise NotImplementedError()

    def abbruch(self):
        self.weiter = False
