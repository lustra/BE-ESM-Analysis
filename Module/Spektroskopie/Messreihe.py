# coding=utf-8
"""
@author: Valon Lushta
@author: Sebastian Badur
"""


class Messreihe:
    def __init__(self, wert):
        self._wert = wert
        self._param = []
        self._reihe = []

    @property
    def wert(self):
        return self._wert

    def add(self, reihe):
        self._param.append(reihe.wert)
        self._reihe.append(reihe)

    def get(self, wert):
        return self._reihe[self._param.index(wert)]


class Omega(Messreihe):
    def __init__(self, wert, ac):
        """
        :type wert: int
        :type ac: AC
        """
        Messreihe.__init__(self, wert)
        self.ac = ac


class AC(Messreihe):
    def __init__(self, wert, dc):
        """
        :type wert: float
        :type dc: DC
        """
        Messreihe.__init__(self, wert)
        self.dc = dc


class DC(Messreihe):
    def __init__(self, wert, messung, fit):
        """
        :type wert: float
        :type messung: numpy.multiarray.ndarray
        :type fit: numpy.multiarray.ndarray
        """
        Messreihe.__init__(self, wert)
        self.messung = messung
        self.fit = fit
