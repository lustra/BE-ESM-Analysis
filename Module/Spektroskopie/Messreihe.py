# coding=utf-8
"""
@author: Valon Lushta
@author: Sebastian Badur
"""


class Messreihe:
    def __init__(self):
        self._param = []
        self._reihe = []

    def _get(self, wert):
        return self._reihe[self._param.index(wert)]

    def alle(self):
        """
        :return: [DC0, DC1, ...], komprimiert für alle Elemente aller Reihen in dieser Reihe
        """
        return [element for sub in self._reihe for element in sub.alle()]


class Omega(Messreihe):
    def __init__(self, omega):
        """
        :type omega: int
        """
        Messreihe.__init__(self)
        self.omega = omega

    def ac(self, wert):
        return self._get(wert)


class AC(Omega):
    def __init__(self, omega, ac):
        """
        :type omega: int
        :type ac: float
        """
        Omega.__init__(self, omega)
        self.ac = ac

        # Diese Listen werden mit den Messwerten (abh. von f) beim Einlesen der Dateien gefüllt
        self.dc = []
        self.amp_freq = []
        self.phase_freq = []

        # Diese Listen werden erst beim Fit mit den Fitparametern (konst.) gefüllt
        self.amp_dc = []
        self.resfreq_dc = []
        self.phase_dc = []

    def alle(self):
        return [self]
