# coding=utf-8
"""
@author: Valon Lushta
@author: Sebastian Badur
"""


class Parameter:
    """ Alle nötigen Messparameter """
    def __init__(self, verzeichnis, pixel, messpunkte, fmin, fmax, errorfunc, fenster, ordnung):
        self.verzeichnis = verzeichnis
        self.pixel = pixel
        self.messpunkte = messpunkte
        self.fmin = fmin
        self.fmax = fmax
        self.errorfunc = errorfunc
        self.fenster = fenster
        self.ordnung = ordnung


class Fehler(Exception):
    pass
