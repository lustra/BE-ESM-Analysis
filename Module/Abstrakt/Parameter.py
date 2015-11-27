# coding=utf-8
"""
@author: Valon Lushta
@author: Sebastian Badur
"""

import os


class Parameter:
    """ Alle für den Fit einer Rastermessung nötigen Messparameter """
    def __init__(self, verzeichnis, fmin, fmax, fitfunktion, fenster, ordnung, phase_versatz):
        """
        :type verzeichnis: str
        :type fmin: float
        :type fmax: float
        :type fenster: int
        :type ordnung: int
        :type phase_versatz: int
        """
        self.verzeichnis = verzeichnis if verzeichnis.endswith(os.sep) else verzeichnis + os.sep
        self.fmin = fmin
        self.fmax = fmax
        self.fitfunktion = fitfunktion
        self.fenster = fenster
        self.ordnung = ordnung
        self.phase_versatz = phase_versatz
