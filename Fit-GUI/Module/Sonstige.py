# coding=utf-8
class Parameter:
    """ Alle nötigen Messparameter """
    def __init__(self, verzeichnis, pixel, messpunkte, fmin, fmax):
        self.verzeichnis = verzeichnis
        self.pixel = pixel
        self.messpunkte = messpunkte
        self.fmin = fmin
        self.fmax = fmax


class Fehler(Exception):
    pass
