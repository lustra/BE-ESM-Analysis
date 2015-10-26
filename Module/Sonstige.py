# coding=utf-8
"""
@author: Valon Lushta
@author: Sebastian Badur
"""


class Parameter:
    """ Alle nötigen Messparameter """
    def __init__(self, verzeichnis, pixel, messpunkte, fmin, fmax, errorfunc, fenster, ordnung):
        """
        :type verzeichnis: str
        :type pixel: int
        :type messpunkte: int
        :type fmin: float
        :type fmax: float
        :type fenster: int
        :type ordnung: int
        """
        self.verzeichnis = verzeichnis
        self.pixel = pixel
        self.messpunkte = messpunkte
        self.fmin = fmin
        self.fmax = fmax
        self.errorfunc = errorfunc
        self.fenster = fenster
        self.ordnung = ordnung


class Achsenbeschriftung:
    def __init__(self, x, y, farbe=None):
        """
        :type x: str
        :type y: str
        :type farbe: str
        """
        self.x = x
        self.y = y
        self.farbe = farbe


class Fehler(Exception):
    pass
