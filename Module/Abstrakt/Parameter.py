# coding=utf-8
"""
@author: Valon Lushta
@author: Sebastian Badur
"""

import os

from Module.Sonstige import Fehler


class Parameter:
    """ Alle für den Fit einer Rastermessung nötigen Messparameter """
    def __init__(self, verzeichnis, fmin, fmax, fitfunktion, fenster, ordnung, phase_modus, phase_versatz):
        """
        :type verzeichnis: str
        :type fmin: float
        :type fmax: float
        :param fitfunktion: Mit den Parametern Frequenz, Resonanzfrequenz, Amplitude, Güte und Offset
        :type fitfunktion: (float, float, float, float, float) -> float
        :type fenster: int
        :type ordnung: int
        :param phase_modus: Der Parameter 'modus' der Funktion Module.Phase.phase_ermitteln()
        :type phase_modus: int
        :type phase_versatz: int
        """
        if fmin >= fmax:
            raise Fehler()

        self.verzeichnis = verzeichnis if verzeichnis.endswith(os.sep) else verzeichnis + os.sep
        self.fmin = fmin
        self.fmax = fmax
        self.fitfunktion = fitfunktion
        self.fenster = fenster
        self.ordnung = ordnung
        self.phase_modus = phase_modus
        self.phase_versatz = phase_versatz
