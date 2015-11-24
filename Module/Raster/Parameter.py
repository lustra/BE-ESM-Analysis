# coding=utf-8
"""
@author: Valon Lushta
@author: Sebastian Badur
"""

from Module.Abstrakt.Parameter import Parameter as AbstraktParameter


class Parameter(AbstraktParameter):
    """ Alle für den Fit einer Rastermessung nötigen Messparameter """
    def __init__(self, verzeichnis, fmin, fmax, fitfunktion, fenster, ordnung,
                 pixel, messpunkte):
        """
        :type pixel: int
        :type messpunkte: int
        """
        AbstraktParameter.__init__(self, verzeichnis, fmin, fmax, fitfunktion, fenster, ordnung)
        self.messpunkte = messpunkte
        self.pixel = pixel
