# coding=utf-8
"""
@author: Valon Lushta
@author: Sebastian Badur
"""


class Parameter:
    """ Alle für den Fit einer Rastermessung nötigen Messparameter """
    def __init__(self, verzeichnis, fmin, fmax, fitfunktion, fenster, ordnung):
        """
        :type verzeichnis: str
        :type fmin: float
        :type fmax: float
        :type fenster: int
        :type ordnung: int
        """
        self.verzeichnis = verzeichnis
        self.fmin = fmin
        self.fmax = fmax
        self.fitfunktion = fitfunktion
        self.fenster = fenster
        self.ordnung = ordnung
